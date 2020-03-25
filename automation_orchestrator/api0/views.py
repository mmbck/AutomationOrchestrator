import json
import pytz
import datetime
import traceback
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from .serializers import ApiTriggerSerializer, BotflowExecutionSerializer, PythonFunctionSerializer, PythonFunctionExecutionSerializer
from orchestrator.models import ApiTrigger, BotflowExecution, PythonFunction, PythonFunctionExecution
from orchestrator.monitoring import add_botflow_execution_object, determine_execution_bot


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class ApiTriggerView(viewsets.ModelViewSet):
    """
    list:
    Return a list of all the existing API triggers.

    retrieve:
    Return and activate the given API trigger.
    """

    queryset = ''
    serializer_class = ApiTriggerSerializer
    throttle_scope = 'apitrigger'
    http_method_names = ['get']

    def list(self, request):
        queryset = ApiTrigger.objects.all()
        serializer = ApiTriggerSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ApiTrigger.objects.exclude(activated=False)
        api_trigger = get_object_or_404(queryset, pk=pk)
        serializer = ApiTriggerSerializer(api_trigger)
        response = serializer.data

        bot = determine_execution_bot(api_trigger)
        response['bot'] = bot.pk

        add_botflow_execution_object(
            bot_pk=bot.pk,
            app_pk=api_trigger.app.pk,
            botflow_pk=api_trigger.botflow.pk,
            trigger=f"API Trigger: {str(pk)}"
        )

        return Response(response)


class BotflowExecutionView(viewsets.ModelViewSet):
    """
    list:
    Return a list of all the existing Botflow execution records.

    retrieve:
    Return the given Botflow execution record.

    partial_update:
    Partially update the Botflow execution record instance.
    """

    queryset = BotflowExecution.objects.all()
    serializer_class = BotflowExecutionSerializer
    throttle_scope = 'botflowexecution'
    http_method_names = ['get', 'patch']
    filterset_fields = ('computer_name', 'user_name', 'status',)

class PythonFunctionView(viewsets.ModelViewSet):
    """
    list:
    Return a list of all the existing Python functions.
    retrieve:
    Return and activate the given Python function.
    """

    queryset = ''
    permission_classes = (IsSuperUser,)
    throttle_scope = 'pythonfunction'
    http_method_names = ['get']

    def list(self, request):
        queryset = PythonFunction.objects.all()
        serializer = PythonFunctionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = PythonFunction.objects.exclude(activated=False)
        item = get_object_or_404(queryset, pk=pk)

        code = item.code
        encrypted_value_1 = item.encrypted_value_1
        encrypted_value_2 = item.encrypted_value_2
        encrypted_value_3 = item.encrypted_value_3
        encrypted_value_4 = item.encrypted_value_4
        encrypted_value_5 = item.encrypted_value_5

        input = self.request.query_params.get('input')

        request_user = request.user

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            request_ip = x_forwarded_for.split(',')[0]
        else:
            request_ip = request.META.get('REMOTE_ADDR')

        execution = log_python_function(
            python_function=item,
            request_user=request_user,
            request_ip=request_ip,
            code=code,
            input=input
        )

        output = {"python_function_execution": execution.pk,
                  "output": exec_python_function(
                      code=code,
                      encrypted_value_1=encrypted_value_1,
                      encrypted_value_2=encrypted_value_2,
                      encrypted_value_3=encrypted_value_3,
                      encrypted_value_4=encrypted_value_4,
                      encrypted_value_5=encrypted_value_5,
                      input=input
                  )
        }

        execution = log_python_function(
            output=output,
            execution=execution
        )

        execution = None
        del execution

        return Response(output)


class PythonFunctionExecutionView(viewsets.ModelViewSet):
    """
    list:
    Return a list of all the existing Python function execution records.
    retrieve:
    Return the given Python function execution record.
    """

    queryset = PythonFunctionExecution.objects.all()
    serializer_class = PythonFunctionExecutionSerializer
    throttle_scope = 'pythonfunctionexecution'
    http_method_names = ['get']


def exec_python_function(code, encrypted_value_1, encrypted_value_2, encrypted_value_3, encrypted_value_4, encrypted_value_5, input):
    output = {}

    try:
        exec(code, locals(), output)
        output = output.get('output')

    except:
        output = traceback.format_exc()

    return output


def log_python_function(python_function=None, request_user=None, request_ip=None, code=None, input=None, output=None, execution=None):
    if execution is None:
        execution = PythonFunctionExecution(
            python_function=python_function,
            request_user=request_user,
            request_ip=request_ip,
            code=code,
            input=input,
            time_start = datetime.datetime.now(pytz.timezone('Europe/Copenhagen')).strftime(f"%Y-%m-%dT%H:%M:%S+0{str(int(datetime.datetime.now(pytz.timezone('Europe/Copenhagen')).utcoffset().seconds / 60 / 60))}00")
        )
        execution.save()

        return execution

    else:
        execution.output = output
        execution.time_end = datetime.datetime.now(pytz.timezone('Europe/Copenhagen')).strftime(f"%Y-%m-%dT%H:%M:%S+0{str(int(datetime.datetime.now(pytz.timezone('Europe/Copenhagen')).utcoffset().seconds / 60 / 60))}00")
        execution.save()

        return execution

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import PatientSerializer
from .paginations import PatientPaginator
from .models import Patient
from rest_framework.permissions import IsAuthenticated

class PatientView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self ,request):
        name = request.query_params.get('name')
        if name:
            patients = Patient.objects.filter(name__icontains=name)
        else:
            patients = Patient.objects.all()
        paginator = PatientPaginator()
        page = paginator.paginate_queryset(patients, request)
        patientsserializer = PatientSerializer(page, many=True)
        return Response(patientsserializer.data, status=status.HTTP_200_OK)
    
    def post(self ,request):
        patientserializer = PatientSerializer(data=request.data)
        if patientserializer.is_valid():
            return Response(patientserializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(patientserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PatientViewDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            patient = Patient.objects.get(pk=id)
        except Patient.DoesNotExist:
            return Response({"message": "Paciente não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        patientserializer = PatientSerializer(patient)
        return Response(patientserializer.data, status=status.HTTP_202_ACCEPTED)
    
    def put(self, request, id):
        try:
            patient = Patient.objects.get(pk=id)
        except Patient.DoesNotExist:
            return Response({"message": "Paciente não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        patientserializer = PatientSerializer(patient, data=request.data)
        if patientserializer.is_valid():
            return Response(patientserializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            patient = Patient.objects.get(pk=id)
        except Patient.DoesNotExist:
            return Response({"message": "Paciente não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        patient.delete()
        return Response({"message": "Paciente deletado com sucesso."}, status=status.HTTP_204_NO_CONTENT)

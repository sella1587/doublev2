from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from .models import Destination

class ImportJsonView(APIView):
    parser_classes = [MultiPartParser]  # Permet de gérer les fichiers téléversés

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # Chargement du fichier JSON
        file = request.FILES['file']
        try:
            import json
            data = json.load(file)
        except Exception:
            return Response({"error": "Invalid JSON file"}, status=status.HTTP_400_BAD_REQUEST)

        # Vérification et mise à jour des données
        source_references = {item['reference'] for item in data}
        Destination.objects.all().update(flagged=True)
        for item in data:
            Destination.objects.update_or_create(
                reference=item['reference'],
                defaults={'name': item['name'], 'flagged': False}
            )

        return Response({"message": "Data imported and flagged successfully"})


from datetime import date
from django.utils.timezone import now


def merge_objects_from_json(source_data):
    """
    Fonction qui effectue le traitement de fusion :
    - Met à jour les objets existants
    - Insère les nouveaux objets
    - Flague les objets absents
    """

    # Récupérer les UIDs de la source
    source_uids = {item['uid'] for item in source_data}

    # Récupérer les objets existants dans la base
    existing_objects = ObjectsFromCao.objects.filter(uid__in=source_uids)

    # Mise à jour des objets existants
    for obj in existing_objects:
        data = next(item for item in source_data if item['uid'] == obj.uid)
        obj.source = data['source']
        obj.name = data['name']
        obj.component_type = data.get('component_type')
        obj.description = data.get('description')
        obj.trade = data.get('trade')
        obj.function = data.get('function')
        obj.lot = data.get('lot')
        obj.room = data.get('room')
        obj.code_client_ouvrage = data.get('code_client_ouvrage')
        obj.code_client_object = data.get('code_client_object')
        obj.code_fournisseur = data.get('code_fournisseur')
        obj.date_last_modified = now()
        obj.save()

    # Insérer les nouveaux objets
    existing_uids = {obj.uid for obj in existing_objects}
    new_objects = [
        ObjectsFromCao(
            uid=item['uid'],
            source=item['source'],
            name=item['name'],
            component_type=item.get('component_type'),
            description=item.get('description'),
            trade=item.get('trade'),
            function=item.get('function'),
            lot=item.get('lot'),
            room=item.get('room'),
            code_client_ouvrage=item.get('code_client_ouvrage'),
            code_client_object=item.get('code_client_object'),
            code_fournisseur=item.get('code_fournisseur'),
            creation_date=now(),
        )
        for item in source_data
        if item['uid'] not in existing_uids
    ]
    ObjectsFromCao.objects.bulk_create(new_objects)

    # Flager les objets absents dans la source
    ObjectsFromCao.objects.filter(
        uid__in=existing_uids - source_uids
    ).update(archived_date=date.today())

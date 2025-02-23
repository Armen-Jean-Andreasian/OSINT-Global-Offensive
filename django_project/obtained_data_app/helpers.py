from django.utils.timezone import now

from obtained_data_app.models import ObtainedDataModel


def extract_user_data(request, logger_entry):
    """
    Extracts user data from the request and logs it in the ObtainedDataModel.
    """
    client_ip = request.headers.get('X-Forwarded-For', request.META.get('REMOTE_ADDR'))
    if ',' in client_ip:
        client_ip = client_ip.split(',')[0]  # Use the first IP in the list

    ObtainedDataModel.objects.create(
        logger=logger_entry,
        date_time=now(),
        ip=client_ip,
        browser=request.headers.get('Sec-Ch-Ua', ''),
        operating_system=request.headers.get('Sec-Ch-Ua-Platform', ''),
        user_agent=request.headers.get('User-Agent', ''),
        host_name=request.get_host(),
        isp=request.headers.get('X-Forwarded-Host', ''),
    )

# from django.views import View
# from django.http import HttpRequest
# from components import JwtToken
#
# class DataObtainerView(View):
#     # TODO: @app.get('/<dynamic_id>') bind this to obtainer/<dynamic_id> url
#     def get(self, request: HttpRequest):
#         request_data = {
#             "method": request.method,
#             "headers": dict(request.headers),
#             "args": request.args.to_dict(),
#             "form": request.form.to_dict(),
#             "json": request.get_json(silent=True),
#             "data": request.data.decode('utf-8'),
#             "cookies": request.cookies,
#             "url": request.url,
#             "base_url": request.base_url,
#             "path": request.path,
#             "query_string": request.query_string.decode('utf-8'),
#             "remote_addr": request.remote_addr,
#             "user_agent": str(request.user_agent),
#         }
#
#
#         client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
#
#         if ',' in client_ip:
#             client_ip = client_ip.split(',')[0]  # Use the first IP in the list
#         print(f"Client IP: {client_ip}")  # Print the actual client IP
#
#         # TODO: extract dynamic_id
#
#         logger_entry = Logger.get_or_none(id=dynamic_id)
#         if logger_entry and logger_entry.destination:
#             # TODO: return html with js code inside that will obtain additional data and redirect
#             return redirect(logger_entry.destination)  # instead of this line
#             # return render(fake_destination.html) rendering fake html
#             # recieve otbained data by fake_destination.html
#             # may be done using get and post methods and logger id:
#             # logger = SELECT * from Logger where id = dynamic_id
#             # also we generate a unique token that we provide to frontend, that has ttl of 1 minute
#             # - in get we render a return render(fake_destination.html, logger_id=logger.id, token=token)
#             # - then the html should send a post to this view class with obatained data and logger id
#
#         return jsonify({"error": "Destination not found"}), 404
#
#
#     def post(self, request: HttpRequest):
#         """
#         For HTML to send obtained data and here we recieve it
#         """
#         # extract token from request
#         token = ...
#
#         if JwtToken.validate(token):
#             # pass here for now, db changes should be done
#         else:
#             return
#
#
#
# #

from .models import ObtainedDataModel
from logger_app.models import LoggerModel
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods


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


@require_http_methods(["GET"])
def redirect_to_destination(request, dynamic_id):
    """
    Redirects to the destination URL if the logger entry exists.
    Logs metadata in ObtainedDataModel.
    """
    try:
        logger_entry = LoggerModel.objects.get(id=dynamic_id)
    except LoggerModel.DoesNotExist:
        return JsonResponse({"error": "Destination not found"}, status=404)

    # Log request metadata
    extract_user_data(request, logger_entry)

    # Redirect to destination
    return HttpResponseRedirect(logger_entry.destination)

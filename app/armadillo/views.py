from django.template.response import TemplateResponse
from django.http import HttpResponse, Http404
import urllib.request, json
from .utils import create_qr_from_text, put_qr_on_marker
from django.conf import settings
from django.templatetags.static import static
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64


def index(request):
    context = {}
    return TemplateResponse(request, 'index.html', context)

def image(request, image=''):
    # query neurovault image
    fileUrl = f"https://neurovault.org/api/images/{image}"
    try:
        with urllib.request.urlopen(fileUrl) as url:
            fileData = json.loads(url.read().decode())
    except (urllib.error.HTTPError, ValueError):
        fileData = None

    # parse image

    # colour file
    # surface_left_file =  fileData['surface_left_file']
    # surface_right_file = fileData['surface_right_file']

    # if surface_left_file != None & surface_right_file != None

    # create QR code

    context = {}
    return TemplateResponse(request, 'index.html', context)

def test(request, image=''):

    qr_link = settings.BASE_URL + '/test/image'
    # qr_code = create_qr_from_text(qr_link)
    marker_with_qr = put_qr_on_marker(qr_link, 'staticfiles/img/marker.png')
    
    pillow_image = ContentFile(base64.b64decode(marker_with_qr), name='temp.jpg')
    image_file = InMemoryUploadedFile(pillow_image, None, 'foo.jpg', 'image/jpeg', pillow_image.tell, None)

    # context = {'img_str': marker_with_qr}
    context = {'img_str': HttpResponse(ContentFile(marker_with_qr), content_type="image/jpeg")}

    # return TemplateResponse(request, 'test.html', context)

    return HttpResponse(image_file, content_type="image/jpeg")



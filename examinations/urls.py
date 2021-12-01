# ----------------------------------------------
# author: Hubert Decyusz
# description: File registers api endpoints
# for model methods usage.

from rest_framework.routers import SimpleRouter
from .views import ExaminationViewSet

router = SimpleRouter()
router.register(r'examinations', ExaminationViewSet, basename='examinations')

urlpatterns = router.urls

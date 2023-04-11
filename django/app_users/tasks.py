from __future__ import absolute_import, unicode_literals

from celery import shared_task
from cloudinary import uploader


@shared_task(name="destroy_profilepicture_on_cloud")
def destroy_profilepicture_on_cloud(public_id):
    uploader.destroy(public_id)
    return {"message": f"profile on cloud storage destroyed!"}

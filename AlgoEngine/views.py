# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dicomdb.utils import getImageBlock

import os
from upload.models import *

from dsrt.settings import STATIC_ROOT
PatientDirBase = os.path.join(STATIC_ROOT, 'data') 

import matplotlib
matplotlib.use('SVG')
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse



# Create your views here.
def make_ct_image(current_ct, ct_block):
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	fig.subplots_adjust(wspace=0, hspace=0)
	ax.imshow(ct_block[:, :, current_ct], cmap='gray')
	ax.axis('off')
	plt.tight_layout()
	img = BytesIO()
	fig.savefig(img, format="png", bbox_inches='tight', pad_inches=0, transparent=True)
	return img


def update_ct(request, patient_id, study_id, series_id, roi_index, index, checked):
	patient = Patient.objects.get(id=patient_id)
	rootDir = os.path.join(PatientDirBase, patient.PatientName)
	cts, _ = getImageBlock(rootDir, patient_id, study_id, series_id)
	checkBox = False
	if "true" in checked:
		checkBox = True

	# Overlay the contour if selected

	current_ct = int(index)
	image = make_ct_image(current_ct, cts)
	return HttpResponse(image.getvalue(), content_type="image/png")

@login_required(login_url='/users/login/')
def get_ct(request, patient_id, study_id, series_id):
	patient = Patient.objects.get(id=patient_id)
	rootDir = os.path.join(PatientDirBase, patient.PatientName)
	if request.method == "GET":
		cts, _ = getImageBlock(rootDir, patient_id, study_id, series_id)
		current_ct = 0
		image = make_ct_image(current_ct, cts)
		return HttpResponse(image.getvalue(), content_type="image/png")
	else:
		return HttpResponse(status=401)


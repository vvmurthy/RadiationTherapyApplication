
from upload.models import RTPlan, PatientSetup
from django.core.exceptions import ObjectDoesNotExist

def parse(dataframe,user,patient,study,series):
	# TODO: fill out fields of RT Plan


	# Fill the Tolerance Table parameters
	try:
		plan = RTPlan.objects.get(fk_study_id=study, fk_patient_id=patient)
	except ObjectDoesNotExist:
		plan = RTPlan()
		plan.fk_study_id = study
		plan.fk_patient_id = patient


		seq = dataframe.ToleranceTableSequence[0]

		for beam_limiting in seq.BeamLimitingDeviceToleranceSequence:
			if beam_limiting.RTBeamLimitingDeviceType == "MLCX":
				plan.limit_mlcx = beam_limiting.BeamLimitingDevicePositionTolerance
			elif beam_limiting.RTBeamLimitingDeviceType == "MLCY":
				plan.limit_mlcy = beam_limiting.BeamLimitingDevicePositionTolerance
			elif beam_limiting.RTBeamLimitingDeviceType == "ASYMX":
				plan.asymx = beam_limiting.BeamLimitingDevicePositionTolerance
			elif beam_limiting.RTBeamLimitingDeviceType == "ASYMY":
				plan.asymy = beam_limiting.BeamLimitingDevicePositionTolerance
			elif beam_limiting.RTBeamLimitingDeviceType == "X":
				plan.x = beam_limiting.BeamLimitingDevicePositionTolerance
			elif beam_limiting.RTBeamLimitingDeviceType == "Y":
				plan.y = beam_limiting.BeamLimitingDevicePositionTolerance

		# Fill the Patient Setup params
		setup = ""
		for setup in dataframe.PatientSetupSequence:
			patient_setup = PatientSetup()
			patient_setup.patient_position = setup.PatientPosition
			patient_setup.patient_setup_number = setup.PatientSetupNumber
			patient_setup.setup_technique = setup.SetupTechnique
			patient_setup.setup_technique_description = setup.SetupTechniqueDescription
			patient_setup.save()

			setup += str(patient_setup.id) + ","
		plan.setup_sequence = setup 

		# Fill in the fraction group sequence
		fraction_group = ""
		f_group = dataframe.FractionGroupSequence[0]
		for setup in f_group:
			dosage = FractionGroupSequence()
			dosage.beam_dose = setup.BeamDose
			dosage.referenced_beam_number = setup.ReferencedBeamNumber
			dosage.beam_meterset = setup.BeamMeterset
			dosage.save()
			fraction_group += str(dosage.id) + ","
		plan.fraction_group_sequence = fraction_group

		# TODO: fill in beam sequence

		# save the object
		plan.save()

	return True
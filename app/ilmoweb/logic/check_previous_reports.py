"""Module for app logic."""
from django.contrib import messages
from ilmoweb.models import Report

def check_and_replace(request, prev, student, lab_group, file): # pylint: disable=too-many-arguments
    """
        Check for previous reports before saving a report
    """
    if prev.exists():

        if prev[0].report_status == 4:
            messages.warning(request, "Et voi palauttaa tähän työhön uutta raporttia")
            return

        prev_comments = prev[0].comments
        prev_comment_file = prev[0].comment_file
        prev_comment_file_name = prev[0].comment_file_name
        prev_notes = prev[0].notes
        report_status = 0
        message = ""

        if prev[0].report_status == 3:
            message = "Korjausehdotukset sisältävä tiedosto korvattu uudella"
            report_status = 3

        if prev[0].report_status == 2:
            message = "Korjausehdotukset sisältävä tiedosto lähetetty onnistuneesti"
            report_status = 3

        if prev[0].report_status == 1:
            message = "Alkuperäisen korvaava tiedosto lähetetty onnistuneesti"
            report_status = 1


        Report.objects.filter(pk=prev[0].id).delete()
        report = Report(student=student,
                        lab_group=lab_group,
                        report_file=file,
                        report_file_name=file.name,
                        report_status=report_status,
                        comments=prev_comments,
                        comment_file=prev_comment_file,
                        comment_file_name=prev_comment_file_name,
                        notes=prev_notes,
                        graded_by=lab_group.assistant)
        report.save()


        messages.success(request, message)
        return

    report = Report(student=student,
                    lab_group=lab_group,
                    report_file=file,
                    report_file_name=file.name,
                    report_status=1,
                    graded_by=lab_group.assistant)
    report.save()
    messages.success(request, "Tiedosto lähetetty onnistuneesti")
    return


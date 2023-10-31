from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from django.test import TestCase, Client
from ilmoweb.models import User, Courses, Labs, LabGroups, Report
from ilmoweb.logic import labgroups
import datetime

class FirstTest(TestCase):
    def setUp(self):
        self.testApp = "IlmoWeb"

    def test_mock_test(self):
        self.assertEqual(self.testApp, "IlmoWeb")

class TestModels(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            student_id = 100111222,
            username = "pvirtanen",
            password = make_password("virtanen"),
            first_name = "Pekka",
            last_name = "Virtanen",
            email = "pekka.virtanen@ilmoweb.fi"
        )

        self.course1 = Courses.objects.create(
            name = "Kemian Labratyö",
            description = "Kemian Labratyö-kurssi",
            labs_amount = 2,
            is_visible = False
        )

        # visible lab
        self.lab1 = Labs.objects.create(
            course = self.course1,
            name = "Kemian Labratyö-kurssi labra 1",
            description = "Labratyö-kurssin ensimmäinen labra",
            max_students = 20,
            is_visible = True
        )

        # invisible lab
        self.lab2 = Labs.objects.create(
            course = self.course1,
            name = "Kemian Labratyö-kurssi labra 2",
            description = "Labratyö-kurssin toinen labra",
            max_students = 20,
            is_visible = False
        )

        # empty labgroup
        self.labgroup1 = LabGroups.objects.create(
            lab = self.lab1,
            date = "2023-06-01",
            start_time = "14:30",
            end_time = "16:30",
            place = "Chemicum",
            status = False
        )

        # nonempty labgroup
        self.labgroup2 = LabGroups.objects.create(
            lab = self.lab1,
            date = "2023-06-02",
            start_time = "14:30",
            end_time = "16:30",
            place = "Chemicum",
            status = False,
            signed_up_students = 1
        )

        # report for testing
        self.report1 = Report.objects.create(
            student = self.user1,
            lab_group = self.labgroup1,
            send_date = "2023-06-10",
            filename = "raportti.pdf",
            report_status = 1,
            comments = "",
        )

        # creating a superuser for testing login
        self.superuser1 = User.objects.create_superuser(
            username = "kemianope",
            password = "atomi123"
        )
        self.superuser1.save()

        self.client=Client()

    # Tests for User-model
    def test_user_is_created_with_correct_id(self):
        self.assertEqual(self.user1.student_id, 100111222)

    def test_user_is_created_with_correct_username(self):
        self.assertEqual(self.user1.username, "pvirtanen")

    def test_user_is_created_with_correct_password(self):
        self.assertTrue(check_password("virtanen", self.user1.password))

    def test_user_is_created_with_correct_name(self):
        self.assertEqual(self.user1.first_name, "Pekka")

    def test_user_is_created_with_correct_surname(self):
        self.assertEqual(self.user1.last_name, "Virtanen")

    def test_user_is_created_with_correct_email(self):
        self.assertEqual(self.user1.email, "pekka.virtanen@ilmoweb.fi")

    # Tests for Courses-model
    def test_course_is_created_with_correct_name(self):
        self.assertEqual(self.course1.name, "Kemian Labratyö")

    def test_course_is_created_with_correct_description(self):
        self.assertEqual(self.course1.description, "Kemian Labratyö-kurssi")

    def test_course_is_created_with_correct_labs_amount(self):
        self.assertEqual(self.course1.labs_amount, 2)

    def test_course_is_created_with_correct_is_visible_value(self):
        self.assertFalse(self.course1.is_visible)

    # Tests for Labs-model
    def test_lab_is_created_with_correct_name(self):
        self.assertEqual(self.lab1.course, self.course1)

    def test_lab_is_created_with_correct_name(self):
        self.assertEqual(self.lab1.name, "Kemian Labratyö-kurssi labra 1")

    def test_lab_is_created_with_correct_description(self):
        self.assertEqual(self.lab1.description, "Labratyö-kurssin ensimmäinen labra")

    def test_lab_is_created_with_correct_max_students_value(self):
        self.assertEqual(self.lab1.max_students, 20)

    def test_lab_is_created_with_correct_is_visible_value(self):
        self.assertTrue(self.lab1.is_visible)

    # Tests for LabGroups
    def test_lab_group_is_created_with_correct_lab(self):
        self.assertEqual(self.labgroup1.lab, self.lab1)

    def test_lab_group_is_created_with_correct_date(self):
        self.assertEqual(self.labgroup1.date, "2023-06-01")

    def test_lab_group_is_created_with_correct_start_time(self):
        self.assertEqual(self.labgroup1.start_time, "14:30")

    def test_lab_group_is_created_with_correct_end_time(self):
        self.assertEqual(self.labgroup1.end_time, "16:30")

    def test_lab_group_is_created_with_correct_place(self):
        self.assertEqual(self.labgroup1.place, "Chemicum")

    def test_lab_group_is_created_with_correct_is_visible_value(self):
        self.assertEqual(self.labgroup1.status, 0)

    # Tests for logging in as superuser
    def test_login_for_superuser(self):
        logged_in = self.client.login(username='kemianope', password='atomi123')
        self.assertTrue(logged_in)

    def test_login_with_wrong_password(self):
        logged_in = self.client.login(username='kemianope', password='chemicum')
        self.assertFalse(logged_in)

    def test_login_as_not_superuser(self):
        logged_in = self.client.login(username=self.user1.username, password=self.user1.password)
        self.assertFalse(logged_in)

    def test_respond_with_correct_status_code_login(self):
        response_get = self.client.get("/accounts/login/",
                                    {'username':'kemianope', 'password':'atomi123'})
        status_code_get = response_get.status_code
        self.assertEqual(status_code_get, 200) # 200 OK

        response_post = self.client.post("/accounts/login/",
                                    {'username':'kemianope', 'password':'atomi123'})
        status_code_post = response_post.status_code
        self.assertEqual(status_code_post, 302) # 302 Found

    def test_logout(self):
        logged_in = self.client.login(username='kemianope', password='atomi123')
        logged_in = self.client.logout()
        self.assertFalse(logged_in)

    def test_respond_with_correct_status_code_logout(self):
        response_get = self.client.get("/accounts/logout/",
                                    {'username':'kemianope', 'password':'atomi123'})
        status_code_get = response_get.status_code
        self.assertEqual(status_code_get, 302) # 302 Found

    # Tests for labgroup enrollment

    def test_student_can_enroll_to_labgroup(self):
        self.client.force_login(self.user1)
        data = {
            'user_id': self.user1.id,
            'group_id': self.labgroup1.id
        }
        response_post = self.client.post('/open_labs/', data, 'application/json')
        self.assertEqual(response_post.status_code, 200)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.signed_up_students, 1)
    
    def test_teacher_cannot_enroll_to_labgroup(self):
        self.client.force_login(self.superuser1)
        data = {
            'user_id': self.superuser1.id,
            'group_id': self.labgroup1.id
        }
        response_post = self.client.post('/open_labs/', data, 'application/json')
        self.assertEqual(response_post.status_code, 400)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.signed_up_students, 0)
    
    def test_student_cannot_enroll_twice_to_same_labgroup(self):
        self.client.force_login(self.user1)
        data = {
            'user_id': self.user1.id,
            'group_id': self.labgroup1.id
        }
        self.client.post('/open_labs/', data, 'application/json')
        with self.assertRaises(ValueError):
            self.client.post('/open_labs/', data, 'application/json')
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.signed_up_students, 1)

    # Tests for confirming labgroup
    
    def test_teacher_can_confirm_nonempty_labgroup(self):
        self.client.force_login(self.superuser1)
        response_post = self.client.post('/open_labs/confirm/', self.labgroup2.id, 'application/json')
        self.assertEqual(response_post.status_code, 302)
        self.labgroup2.refresh_from_db()
        self.assertEqual(self.labgroup2.status, 2)
    
    def test_teacher_cannot_confirm_empty_labgroup(self):
        self.client.force_login(self.superuser1)
        response_post = self.client.post('/open_labs/confirm/', self.labgroup1.id, 'application/json')
        self.assertEqual(response_post.status_code, 400)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.status, False)
    
    def test_student_cannot_confirm_labgroup(self):
        self.client.force_login(self.user1)
        response_post = self.client.post('/open_labs/confirm/', self.labgroup1.id, 'application/json')
        self.assertEqual(response_post.status_code, 400)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.status, False)

    # Tests for reports
    def test_report_is_saved_to_db(self):
        self.all_reports = Report.objects.all()
        self.assertEqual(len(self.all_reports), 1)

    def test_saved_report_has_correct_fields(self):
        self.all_reports = Report.objects.all()
        self.assertEqual(self.all_reports[0].student, self.user1)
        self.assertEqual(self.all_reports[0].lab_group, self.labgroup1)
        self.assertEqual(self.all_reports[0].filename, "raportti.pdf")
        self.assertEqual(self.all_reports[0].comments, "")
        self.assertEqual(self.all_reports[0].graded_by, None)
    
    # Tests for creating labgroups

    def test_start_end_times_8_to_12(self):
        lab = self.lab1
        date = '2023-10-13'
        time = '8-12'
        place = 'B105'

        labgroups.create(lab, date, time, place)

        group = LabGroups.objects.get(lab=lab, date=date, place=place)

        self.assertEqual(group.start_time.hour, 8)
        self.assertEqual(group.end_time.hour, 12)

    def test_start_end_times_12_to_16(self):
        lab = self.lab1
        date = '2023-10-13'
        time = '12-16'
        place = 'B105'

        labgroups.create(lab, date, time, place)

        group = LabGroups.objects.get(lab=lab, date=date, place=place)

        self.assertEqual(group.start_time.hour, 12)
        self.assertEqual(group.end_time.hour, 16)
    
    def test_labgroup_is_saved_to_db(self):
        lab = self.lab1
        date = '2023-10-13'
        time = '8-12'
        place = 'B105'

        prev = len(LabGroups.objects.all())
        labgroups.create(lab, date, time, place)
        new = len(LabGroups.objects.all())

        self.assertEqual(prev + 1, new)
    
    def test_teacher_can_create_labgroup(self):
        lab = self.lab1.id
        date = '2023-10-13'
        time = '8-12'
        place = 'B105'

        self.client.force_login(self.superuser1)
        prev = len(LabGroups.objects.all())
        get_response = self.client.get("/create_group/", {'course_id':self.course1.id})
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post("/create_group/", {'labs[]':lab, 'place':place, 'date':date, 'time':time})
        self.assertEqual(post_response.status_code, 302)
        new = len(LabGroups.objects.all())
        self.assertEqual(prev + 1, new)

    def test_teacher_can_create_multiple_labgroups(self):
        labs = [self.lab1.id, self.lab2.id]
        date = '2023-10-13'
        time = '8-12'
        place = 'B105'

        self.client.force_login(self.superuser1)
        prev = len(LabGroups.objects.all())
        get_response = self.client.get("/create_group/", {'course_id':self.course1.id})
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post("/create_group/", {'labs[]':labs, 'place':place, 'date':date, 'time':time})
        self.assertEqual(post_response.status_code, 302)
        new = len(LabGroups.objects.all())
        self.assertEqual(prev + 2, new)
    
    def test_student_cannot_access_create_labgroup(self):
        self.client.force_login(self.user1)

        response = self.client.get("/create_group/", {'course_id':self.course1.id})
        self.assertEqual(response.url, '/open_labs')
    
    def test_cannot_create_labgroup_if_not_logged_in(self):
        lab = self.lab1.id
        date = '2023-10-13'
        time = '8-12'
        place = 'B105'

        prev = len(LabGroups.objects.all())
        post_response = self.client.post("/create_group/", {'labs[]':lab, 'place':place, 'date':date, 'time':time})
        self.assertEqual(post_response.status_code, 302)
        new = len(LabGroups.objects.all())
        self.assertEqual(prev, new)

    # Tests for activating labs

    def test_teacher_can_activate_lab(self):
        self.client.force_login(self.superuser1)
        url = reverse('make_lab_visible', args=[str(self.lab2.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab2.refresh_from_db()
        self.assertEqual(self.lab2.is_visible, True)
    
    def test_teacher_can_deactivate_lab(self):
        self.client.force_login(self.superuser1)
        url = reverse('make_lab_visible', args=[str(self.lab1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab1.refresh_from_db()
        self.assertEqual(self.lab1.is_visible, False)
    
    def test_student_cannot_activate_lab(self):
        self.client.force_login(self.user1)
        url = reverse('make_lab_visible', args=[str(self.lab2.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab2.refresh_from_db()
        self.assertEqual(self.lab2.is_visible, False)

    # Tests for deleting labs

    def test_teacher_can_delete_lab(self):
        self.client.force_login(self.superuser1)
        url = reverse('delete_lab', args=[str(self.lab1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab1.refresh_from_db()
        self.assertEqual(self.lab1.deleted, True)
    
    def test_student_cannot_delete_lab(self):
        self.client.force_login(self.user1)
        url = reverse('delete_lab', args=[str(self.lab1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.lab1.refresh_from_db()
        self.assertEqual(self.lab1.deleted, False)

    # Tests for evaluating labs

    def test_teacher_can_evaluate_reports(self):
        self.client.force_login(self.superuser1)
        url = reverse('evaluate_report', args=[str(self.report1.id)])
        response = self.client.post(url, {'grade': 5, 'comments': 'Perfectly done!'})
        self.assertEqual(response.status_code, 302)
        self.report1.refresh_from_db()
        self.assertEqual(self.report1.grade, 5)
        self.assertEqual(self.report1.comments, 'Perfectly done!')
        self.assertEqual(self.report1.graded_by_id, self.superuser1.id)
        self.assertEqual(self.report1.grading_date, datetime.date.today())
        self.assertEqual(self.report1.report_status, 4)
    
    def test_student_cannot_grade_reports(self):
        self.client.force_login(self.user1)
        url = reverse('evaluate_report', args=[str(self.report1.id)])
        response = self.client.post(url, {'grade': 5, 'comments': 'Perfectly done!'})
        self.assertEqual(response.url, '/my_labs' )
    
    def test_teacher_can_send_reports_to_be_fixed(self):
        self.client.force_login(self.superuser1)
        url = reverse('evaluate_report', args=[str(self.report1.id)])
        response = self.client.post(url, {'grade': 0, 'comments': 'Korjaa'})
        self.assertEqual(response.status_code, 302)
        self.report1.refresh_from_db()
        self.assertEqual(self.report1.report_status, 2)
        self.assertEqual(self.report1.comments, 'Korjaa')

    # Test for deleting labgroups

    def test_teacher_can_delete_labgroup(self):
        self.client.force_login(self.superuser1)
        url = reverse('delete_labgroup', args=[str(self.labgroup1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.deleted, True)

    def test_student_cannot_delete_labgroup(self):
        self.client.force_login(self.user1)
        url = reverse('delete_labgroup', args=[str(self.labgroup1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.labgroup1.refresh_from_db()
        self.assertEqual(self.labgroup1.deleted, False)

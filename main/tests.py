import uuid
from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project, Education


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")



## PROJECT API TEST CASE
class ProjectAPITestCase(APITestCase):
    def setUp(self):
        # 1. Buat grup Editor
        self.editor_group = Group.objects.create(name="Editor")
        
        # 2. Buat akun test untuk 4 peran
        self.owner = User.objects.create_superuser(username="owner", password="password123")
        self.editor = User.objects.create_user(username="editor", password="password123")
        self.editor.groups.add(self.editor_group)
        self.regular_user = User.objects.create_user(username="user", password="password123")

        # 3. Data awal Project (UUID)
        self.project = Project.objects.create(
            title="Portfolio Website",
            description="Personal portfolio website developed as part of PBP assignment.",
            tech_stack="Django, Java, HTML, CSS",
            project_url="https://github.com/sofiedaniella-dev/myportofolio",
            project_image_url="https://example.com/image.png"
        )
        self.list_url = "/api/v1/projects/"
        self.detail_url = f"/api/v1/projects/{self.project.pk}/"
        self.star_url = f"/api/v1/projects/{self.project.pk}/star/"

    # Test 1: Pengunjung tanpa login & User biasa ditolak saat menulis data[cite: 14]
    def test_anonymous_and_regular_user_cannot_write(self):
        # Anonymous ditolak saat POST
        res_anon = self.client.post(self.list_url, {
            "title": "Test Project", "description": "Desc", "tech_stack": "Python"
        })
        self.assertEqual(res_anon.status_code, status.HTTP_403_FORBIDDEN)

        # User biasa ditolak saat POST
        self.client.force_authenticate(user=self.regular_user)
        res_user = self.client.post(self.list_url, {
            "title": "Test Project", "description": "Desc", "tech_stack": "Python"
        })
        self.assertEqual(res_user.status_code, status.HTTP_403_FORBIDDEN)

        # Periksa DB: Data tidak bertambah[cite: 14]
        self.assertEqual(Project.objects.count(), 1)

    # Test 2: Editor boleh PATCH, tetapi ditolak saat POST/Create dan DELETE[cite: 14]
    def test_editor_can_patch_but_not_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        # Editor Boleh PATCH
        res_patch = self.client.patch(self.detail_url, {"title": "Updated Portfolio Project"})
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Updated Portfolio Project")

        # Editor Ditolak POST
        res_post = self.client.post(self.list_url, {
            "title": "New Project", "description": "Desc", "tech_stack": "Django"
        })
        self.assertEqual(res_post.status_code, status.HTTP_403_FORBIDDEN)

        # Editor Ditolak DELETE
        res_del = self.client.delete(self.detail_url)
        self.assertEqual(res_del.status_code, status.HTTP_403_FORBIDDEN)

        # Periksa DB: Data masih ada di database[cite: 14]
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())

    # Test 3: Pemilik (Superuser) boleh POST dan DELETE[cite: 14]
    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        # Owner Boleh POST (Create)
        res_post = self.client.post(self.list_url, {
            "title": "New Project", "description": "Desc", "tech_stack": "Django"
        })
        self.assertEqual(res_post.status_code, status.HTTP_201_CREATED)

        # Owner Boleh DELETE
        res_del = self.client.delete(self.detail_url)
        self.assertEqual(res_del.status_code, status.HTTP_204_NO_CONTENT)
        
        # Periksa DB: Data telah terhapus[cite: 14]
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    # Test 4: Validasi Input Teks[cite: 14]
    def test_validation_input(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.post(self.list_url, {
            "title": "   ",  # Title kosong/spasi saja
            "description": "Desc",
            "tech_stack": "Python"
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 5: Star Endpoint[cite: 14]
    def test_star_endpoint(self):
        # Anonymous ditolak star
        res_anon = self.client.post(self.star_url)
        self.assertEqual(res_anon.status_code, status.HTTP_403_FORBIDDEN)

        # User biasa boleh star
        self.client.force_authenticate(user=self.regular_user)
        res_star = self.client.post(self.star_url)
        self.assertEqual(res_star.status_code, status.HTTP_200_OK)
        self.assertTrue(self.project.starred_by.filter(pk=self.regular_user.pk).exists())

    # Test 6: CSRF Enforcement menggunakan APIClient(enforce_csrf_checks=True) & .login()[cite: 14]
    def test_csrf_enforcement(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        csrf_client.login(username="owner", password="password123")
        res = csrf_client.post(self.list_url, {
            "title": "CSRF Project", "description": "Desc", "tech_stack": "Python"
        })
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


## EDUCATION API TEST CASE
class EducationAPITestCase(APITestCase):
    def setUp(self):
        # 1. Buat grup Editor
        self.editor_group = Group.objects.create(name="Editor")
        
        # 2. Buat akun test untuk 4 peran
        self.owner = User.objects.create_superuser(username="owner", password="password123")
        self.editor = User.objects.create_user(username="editor", password="password123")
        self.editor.groups.add(self.editor_group)
        self.regular_user = User.objects.create_user(username="user", password="password123")

        # 3. Buat data awal
        self.edu = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Ilmu Komputer",
            start_year="2025",
            end_year="2029"
        )
        self.list_url = "/api/v1/education/"
        self.detail_url = f"/api/v1/education/{self.edu.pk}/"
        self.star_url = f"/api/v1/education/{self.edu.pk}/star/"

    # Test 1: Pengunjung tanpa login & User biasa ditolak saat menulis data[cite: 14]
    def test_anonymous_and_regular_user_cannot_write(self):
        # Anonymous ditolak
        res_anon = self.client.post(self.list_url, {"institution": "Test Univ", "degree": "S1"})
        self.assertEqual(res_anon.status_code, status.HTTP_403_FORBIDDEN)

        # User biasa ditolak
        self.client.force_authenticate(user=self.regular_user)
        res_user = self.client.post(self.list_url, {"institution": "Test Univ", "degree": "S1"})
        self.assertEqual(res_user.status_code, status.HTTP_403_FORBIDDEN)

        # Periksa isi database (data tidak bertambah)[cite: 14]
        self.assertEqual(Education.objects.count(), 1)

    # Test 2: Editor boleh PATCH, tetapi ditolak saat POST/Create dan DELETE[cite: 14]
    def test_editor_can_patch_but_not_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        # Editor Boleh PATCH
        res_patch = self.client.patch(self.detail_url, {"institution": "UI Fasilkom"})
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.edu.refresh_from_db()
        self.assertEqual(self.edu.institution, "UI Fasilkom")

        # Editor Ditolak POST
        res_post = self.client.post(self.list_url, {"institution": "ITB", "degree": "S1"})
        self.assertEqual(res_post.status_code, status.HTTP_403_FORBIDDEN)

        # Editor Ditolak DELETE
        res_del = self.client.delete(self.detail_url)
        self.assertEqual(res_del.status_code, status.HTTP_403_FORBIDDEN)

        # Periksa isi database (data masih ada)[cite: 14]
        self.assertTrue(Education.objects.filter(pk=self.edu.pk).exists())

    # Test 3: Pemilik (Superuser) boleh POST dan DELETE[cite: 14]
    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        # Owner Boleh POST
        res_post = self.client.post(self.list_url, {
            "institution": "SMA Negeri 1", "degree": "Formal", "start_year": "2022", "end_year": "2025"
        })
        self.assertEqual(res_post.status_code, status.HTTP_201_CREATED)

        # Owner Boleh DELETE
        res_del = self.client.delete(self.detail_url)
        self.assertEqual(res_del.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Education.objects.filter(pk=self.edu.pk).exists())

    # Test 4: Validasi Input[cite: 14]
    def test_validation_input(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.post(self.list_url, {"institution": "", "degree": "S1"})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 5: Star Endpoint[cite: 14]
    def test_star_endpoint(self):
        # Anonymous ditolak star
        res_anon = self.client.post(self.star_url)
        self.assertEqual(res_anon.status_code, status.HTTP_403_FORBIDDEN)

        # User biasa boleh star
        self.client.force_authenticate(user=self.regular_user)
        res_star = self.client.post(self.star_url)
        self.assertEqual(res_star.status_code, status.HTTP_200_OK)
        self.assertTrue(self.edu.starred_by.filter(pk=self.regular_user.pk).exists())

    # Test 6: CSRF Enforcement menggunakan APIClient(enforce_csrf_checks=True) & .login()[cite: 14]
    def test_csrf_enforcement(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        csrf_client.login(username="owner", password="password123")
        res = csrf_client.post(self.list_url, {
            "institution": "Test CSRF", "degree": "S1", "start_year": "2025"
        })
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


## EXPERIENCE API TEST CASE
class ExperienceAPITestCase(APITestCase):
    def setUp(self):
        self.editor_group = Group.objects.create(name="Editor")
        self.owner = User.objects.create_superuser(username="owner", password="password123")
        self.editor = User.objects.create_user(username="editor", password="password123")
        self.editor.groups.add(self.editor_group)
        self.regular_user = User.objects.create_user(username="user", password="password123")

        self.exp = Experience.objects.create(
            title="Software Engineer Intern",
            organization="Tech Corp",
            description="Developing web apps",
            category="internship",
            started_at="2026-01-01T00:00:00Z"
        )
        self.list_url = "/api/v1/experience/"
        self.detail_url = f"/api/v1/experience/{self.exp.pk}/"

    def test_editor_can_patch_experience(self):
        self.client.force_authenticate(user=self.editor)
        res = self.client.patch(self.detail_url, {"title": "Senior Engineer Intern"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.exp.refresh_from_db()
        self.assertEqual(self.exp.title, "Senior Engineer Intern")

    def test_owner_can_delete_experience(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Experience.objects.filter(pk=self.exp.pk).exists()) 


## API TEST
class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
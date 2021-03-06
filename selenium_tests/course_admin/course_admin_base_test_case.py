from os.path import abspath, dirname, join
from urllib.parse import urljoin

from django.conf import settings

from selenium_common.base_test_case import BaseSeleniumTestCase
from selenium_common.canvas.canvas_masquerade_page_object \
    import CanvasMasqueradePageObject
from selenium_common.pin.page_objects.pin_login_page_object import \
    PinLoginPageObject
from selenium_tests.course_admin.page_objects\
    .course_admin_dashboard_page_object import CourseAdminDashboardPage

# Common files used for all Manage Course dashboard test cases:
MANAGE_COURSE_PERMISSIONS = join(
    dirname(abspath(__file__)),
    'test_data',
    'course_admin_roles_access.xlsx')


class CourseAdminBaseTestCase(BaseSeleniumTestCase):

    @classmethod
    def setUpClass(cls):
        super(CourseAdminBaseTestCase, cls).setUpClass()

        cls.USERNAME = settings.SELENIUM_CONFIG['selenium_username']
        cls.PASSWORD = settings.SELENIUM_CONFIG['selenium_password']
        cls.CANVAS_BASE_URL = settings.SELENIUM_CONFIG['canvas_base_url']
        cls.TOOL_RELATIVE_URL = settings.SELENIUM_CONFIG['manage_course'][
            'relative_url']
        cls.TOOL_URL = urljoin(cls.CANVAS_BASE_URL, cls.TOOL_RELATIVE_URL)
        cls.course_admin_dashboard_page = CourseAdminDashboardPage(cls.driver)
        cls.course_admin_dashboard_page.get(cls.TOOL_URL)

        cls.masquerade_page = CanvasMasqueradePageObject(cls.driver,
                                                         cls.CANVAS_BASE_URL)
        login_page = PinLoginPageObject(cls.driver)
        if login_page.is_loaded():
            login_page.login_xid(cls.USERNAME, cls.PASSWORD)
        else:
            print('(User {} already logged in to PIN)'.format(cls.USERNAME))

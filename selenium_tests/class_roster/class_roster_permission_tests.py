from ddt import ddt, data, unpack

from selenium_common.base_test_case import get_xl_data
from selenium_tests.class_roster.class_roster_base_test_case import (
    ClassRosterBaseTestCase,
    CLASS_ROSTER_PERMISSION_ROLES)
from selenium_tests.class_roster.page_objects.class_roster_main_page import \
    MainPageObject


@ddt
class ClassRosterPermissionTests(ClassRosterBaseTestCase):

    @data(*get_xl_data(CLASS_ROSTER_PERMISSION_ROLES))
    @unpack
    def test_roles_access(self, user_id, given_access, expected_role):
        # This test masquerades as users in roles in the spreadsheet
        # specified in CLASS_ROSTER_PERMISSION_ROLES, and then validates the
        # the users are granted/denied access based on their role.

        #  Instantiate
        main_page = MainPageObject(self.driver)

        #  Masquerade as test user
        self.masquerade_page.masquerade_as(user_id)

        # Go back to the Manage Course Dashboard
        self.driver.get(self.TOOL_URL)

        if given_access == 'yes':
            # If user should have access to Class Roster tool, verify
            # that the user sees the class roster button
            self.assertTrue(
                self.course_admin_dashboard_page
                    .class_roster_button_is_displayed(),
                'User {} with expected role {} should see the class roster '
                'button on page but does not'.format(user_id, expected_role)
            )

            # Clicks into tool
            self.course_admin_dashboard_page.select_class_roster_link()

            # Verifies that user can click into and see the class roster tool
            self.assertTrue(main_page.is_loaded())

        elif given_access == 'no':
            self.assertFalse(
                self.course_admin_dashboard_page
                    .class_roster_button_is_displayed(),
                'User {} with expected role {} should not see the class '
                'roster tool, but can see it.'.format(user_id, expected_role)
            )

        else:
            raise ValueError(
                'given_access column for user {} must be either "yes" or '
                '"no"'.format(user_id, expected_role)
            )

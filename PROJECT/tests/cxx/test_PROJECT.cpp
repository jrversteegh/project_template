#include "../test_common.h"

BOOST_AUTO_TEST_CASE(PROJECT_test) {
  BOOST_TEST(true);
}

struct PROJECTFixture {};

BOOST_FIXTURE_TEST_CASE(PROJECT_fixture_test, PROJECTFixture) {
  BOOST_TEST(true);
};

ut::test_suite* init_unit_test_suite(int, char*[]) {
  return 0;
}

from rest_framework.routers import SimpleRouter
from .views import (
    ProjectViewset,
    # ContributorsViewset,
    # IssuesViewset,
    # CommentsViewset,
)

router = SimpleRouter()
router.register("projects", ProjectViewset, basename="projects")
# router.register(
#     r"projects/(?P<project_id>\d+)/users", ContributorsViewset, basename="project-contributors"
# )
# router.register(
#    r"projects/(?P<project_id>\d+)/issues", IssuesViewset, basename="project-issues"
# )
# router.register(
#    r"projects/(?P<project_id>\d+)/issues/(?P<issue_id>\d+)/comments",
#    CommentsViewset,
#    basename="issues-comments",
# )

urlpatterns = router.urls

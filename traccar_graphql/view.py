from flask_graphql import GraphQLView
from flask_jwt_extended import set_access_cookies


class GraphQLViewWithCookie(GraphQLView):
    """
        Sets tokens from flask JWT in cookies
    """

    def dispatch_request(self):
        response = super(GraphQLViewWithCookie, self).dispatch_request()
        if response.status_code == 200:
            context = self.get_context()
            try:
                access_token = getattr(context, "jwt_access_token")
                set_access_cookies(response, access_token)
            except AttributeError:
                pass
        return response

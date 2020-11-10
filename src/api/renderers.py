from rest_framework.renderers import BrowsableAPIRenderer


class NoHTMLFormBrowsableAPIRenderer(BrowsableAPIRenderer):
    OPTIONS_METHOD = "OPTIONS"

    def get_rendered_html_form(self, data, view, method, request):
        if method == self.OPTIONS_METHOD:
            return super().get_rendered_html_form(data, view, method, request)
        else:
            """
            We don't want the HTML forms to be rendered because it can be
            really slow with large datasets
            """
            return ""

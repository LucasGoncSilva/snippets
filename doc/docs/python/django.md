# Django

## Orchestrator

??? example "orchestrator.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/ORCHESTRATOR_orchestrator.py"
    ```

---

## MEDIA and STATIC

??? example "settings.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/MEDIA_STATIC_settings.py"
    ```

??? example "urls.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/MEDIA_STATIC_urls.py"
    ```

---

## Custom User

??? example "models.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/CUSTOM_USER_models.py"
    ```

??? example "forms.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/CUSTOM_USER_forms.py"
    ```

??? example "admin.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/CUSTOM_USER_admin.py"
    ```

??? example "app/urls.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/CUSTOM_USER_app_urls.py"
    ```

??? example "views.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/CUSTOM_USER_views.py"
    ```

??? example "PROJECT/urls.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/CUSTOM_USER_project_urls.py"
    ```

??? example "Reset password HTML snippet"

    ```html
    --8<-- "./docs/examples/python/django/CUSTOM_USER_reset_password_HTML_snippet.html"
    ```

??? example "settings.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/CUSTOM_USER_settings.py"
    ```

---

## E-mail

??? example "settings.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/EMAIL_settings.py"
    ```

??? example "views.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/EMAIL_views.py"
    ```

---

## Messages

??? example "settings.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/MESSAGES_settings.py"
    ```

??? example "Usage `.py` and `.html`"

    ```py title=""
    --8<-- "./docs/examples/python/django/MESSAGES_py_example.py"
    ```

    ```html title=""
    {% if messages %}
        {% for message in messages %}
            <div class='alert {{ message.tags }} mt-3 py-2' role='alert'>{{ message }}</div>
        {% endfor %}
    {% endif %}
    ```

---

## DB Integration

??? example "settings.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/DBINTEGRATION_settings.py"
    ```

---

## Deploy

??? example "deploy.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/DEPLOY_deploy.py"
    ```

---

## Custom err pages

??? example "PROJECT/urls.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/CUSTOM_ERR_PAGES_project_urls.py"
    ```

??? example "app/views.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/CUSTOM_ERR_PAGES_app_views.py"
    ```

## Security

??? example "settings.py"

    ```py title=""
    --8<-- "./docs/examples/python/django/SECURITY_settings.py"
    ```

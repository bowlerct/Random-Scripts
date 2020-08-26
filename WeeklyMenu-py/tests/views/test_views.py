import pytest
from django.urls import reverse


def test_index_view(client):
    response = client.get( reverse('index') ) #index(request)
    assert response.status_code == 200

# use admin_client for admin users
@pytest.mark.django_db()
def test_editmenu_view(auto_login_user):
    client, user = auto_login_user()
    # FIXME pk should be the pk of the recipe not the user
    response = client.get( reverse('editrecipe', kwargs={'pk': user.pk}) ) # /foodmenu/1/edit
    assert response.status_code == 404 # we have not created any recipe's yet

def test_menu_view(auto_login_user):
    client, user = auto_login_user()
    response = client.get( reverse('menu') )
    assert response.status_code == 200

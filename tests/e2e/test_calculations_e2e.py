import time
import pytest

@pytest.mark.e2e
def test_calculation_bread_positive(page, fastapi_server):
    # Register and ensure token stored
    email = f"calc_user_{int(time.time()*1000)}@example.com"
    page.goto('http://127.0.0.1:8000/register')
    page.fill('input#email', email)
    page.fill('input#password', 'password123')
    page.fill('input#confirm', 'password123')
    page.click('button[type="submit"]')
    page.wait_for_function("() => document.querySelector('#message') && document.querySelector('#message').innerText.length > 0")
    assert 'Registration successful' in page.inner_text('#message')
    token = page.evaluate("() => localStorage.getItem('access_token')")
    assert token is not None

    # Go to index and create calculation
    page.goto('http://127.0.0.1:8000')
    page.select_option('select#op', 'add')
    page.fill('input#n1', '4')
    page.fill('input#n2', '6')
    page.click('form#createCalc button[type="submit"]')
    page.wait_for_function("() => document.querySelector('#calcMessage') && document.querySelector('#calcMessage').innerText.length > 0")
    assert 'Created' in page.inner_text('#calcMessage')

    # Wait for list to include the created calculation
    page.wait_for_function("() => document.querySelector('#calcList').innerText.includes('add')")
    assert 'add' in page.inner_text('#calcList')

    # Edit the first calculation in the list
    # click the first Edit button
    page.click('#calcList button:text("Edit")')
    # change values
    page.fill('#calcList input', '10')
    # submit save
    page.click('#calcList button:text("Save")')
    page.wait_for_function("() => document.querySelector('#calcMessage') && document.querySelector('#calcMessage').innerText.includes('Updated')")
    assert 'Updated' in page.inner_text('#calcMessage')

    # Delete the calculation
    # ensure confirm returns true and click delete
    page.evaluate("() => { window.confirm = () => true; }")
    page.click('#calcList button:text("Delete")')
    page.wait_for_function("() => document.querySelector('#calcMessage') && document.querySelector('#calcMessage').innerText.includes('Deleted')")
    assert 'Deleted' in page.inner_text('#calcMessage')


@pytest.mark.e2e
def test_calculation_negative_and_unauthorized(page, fastapi_server):
    # Ensure logged out
    page.goto('http://127.0.0.1:8000/register')
    page.evaluate("() => localStorage.removeItem('access_token')")

    # Go to index and attempt to create without numbers -> client-side validation
    page.goto('http://127.0.0.1:8000')
    page.select_option('select#op', 'add')
    page.fill('input#n1', '')
    page.fill('input#n2', '')
    page.click('form#createCalc button[type="submit"]')
    page.wait_for_function("() => document.querySelector('#calcMessage') && document.querySelector('#calcMessage').innerText.length > 0")
    assert 'Numbers required' in page.inner_text('#calcMessage')

    # Attempt to create while unauthorized (clear token and try with numbers)
    page.fill('input#n1', '1')
    page.fill('input#n2', '2')
    page.evaluate("() => localStorage.removeItem('access_token')")
    page.click('form#createCalc button[type="submit"]')
    page.wait_for_function("() => document.querySelector('#calcMessage') && document.querySelector('#calcMessage').innerText.length > 0")
    # Should show an error from server about authentication
    assert ('Not authenticated' in page.inner_text('#calcMessage')) or ('Invalid token' in page.inner_text('#calcMessage'))

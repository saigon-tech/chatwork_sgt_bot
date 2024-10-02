from src.actions.action_weather import weather_forecast


def test_action_weather():
    message = weather_forecast("ho chi minh")

    assert "Current weather of" in message, "Expected 'Current weather of' to be in response"
    assert "Temperature" in message, "Expected 'Temperature' to be in response"
    assert "°C" in message, "Expected '°C' to be in response"

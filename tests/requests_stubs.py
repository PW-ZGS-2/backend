from telescope.rest_models import TelescopeRequest

post_telescope_stub = TelescopeRequest(telescope_name = "Test Telescope",
telescope_type = "OPEN_SOURCE",
price_per_minute = 1.0,
owner = "John Doe",
status = "FREE",
location = {"city": "Test City", "country": "Test Country", "latitude": 0, "longitude": 0},
specifications = {"aperture": 10.0, "focal_length": 1000.0, "focal_ratio": 1.0, "weight": 5.0,
                  "length": 30.0, "width": 30.0, "height": 30.0, "mount_type": "ALT_AZ", "optical_design": "Reflector"})

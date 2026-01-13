
class GlobalPlugin:
    def script_test(self):
        """Original docstring"""
        pass

# Simulating the assignment at the end of the module
GlobalPlugin.script_test.__doc__ = "Translated docstring"

print(f"Docstring: {GlobalPlugin.script_test.__doc__}")

# Check if instance method sees it
instance = GlobalPlugin()
print(f"Instance Docstring: {instance.script_test.__doc__}")

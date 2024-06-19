from django.shortcuts import render
from .utils import read_model_options_from_excel
import ui.tco_model as tco
import os

def index(request):
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Construct the relative path to the Excel file
    file_path = os.path.join(project_dir, 'coating_details 1.xlsx')
    model_options = read_model_options_from_excel(file_path)
    image_url = None

    if request.method == 'POST':
        form_data = request.POST
        num_rows = len([key for key in form_data if key.startswith('coating_model_')])
        combined_models = []
        message = ""

        try:
            for i in range(num_rows):
                coating_type = form_data.get(f'coating_model_{i}')
                cleaning_option = form_data.get(f'cleaning_option_{i}')
                cleaning_frequency = form_data.get(f'cleaning_frequency_{i}')
                growth_type = form_data.get(f'growth_type_{i}')
                average_power = form_data.get(f'average_power_{i}')
                max_speed = form_data.get(f'max_speed_{i}')
                activity = form_data.get(f'activity_{i}')
                region = form_data.get(f'region_{i}')
                fuel_type = form_data.get(f'fuel_type_{i}')
                fouling_type = form_data.get(f'fouling_type_{i}')

                # Collect additional parameters
                additional_params = {}
                additional_param_keys = form_data.getlist(f'additional_param_{i}')
                additional_param_values = form_data.getlist(f'param_value_{i}')
                for key, value in zip(additional_param_keys, additional_param_values):
                    if value:  # Ensure the value is not empty
                        additional_params[key] = float(value)

                # Define valid parameters for tco_model
                valid_params = {
                    'coating_type': coating_type,
                    'cleaning_frequency': int(cleaning_frequency) if cleaning_option == "Cleaning Frequency" else None,
                    'fixed_cleanings': [int(x) for x in cleaning_frequency.split(',')] if cleaning_option == "Fixed Cleanings" else None,
                    'growth_type': growth_type,
                    'average_power': float(average_power),
                    'max_speed': int(max_speed),
                    'activity_rate': float(activity),
                    'region': region,
                    'fuel_type': fuel_type,
                    'fouling_type': fouling_type,
                    'reactive_cleaning': 10 if cleaning_option == "Reactive Cleaning" else None,
                }
                valid_params.update(additional_params)

                # Filter None values
                model_params = {k: v for k, v in valid_params.items() if v is not None}

                model_instance = tco.tco_model(**model_params)
                combined_models.append(model_instance)

            tco.plot_results_obj_list(models=combined_models, no_power_details=False, col="power_change", growth_type=growth_type, save=True)
            image_url = 'static/ui/simulation_results.png'
            message = "Simulation completed successfully."
        except Exception as e:
            message = f"An error occurred: {e}"

        return render(request, 'ui/index.html', {'model_options': model_options, 'message': message, 'image_url': image_url})

    return render(request, 'ui/index.html', {'model_options': model_options})

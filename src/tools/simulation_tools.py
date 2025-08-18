import numpy as np
import math
import random
from typing import Dict, List, Tuple, Any
from langchain.tools import BaseTool, tool
import json

class GenericSimulator:
    """Generic simulation engine for various scientific domains"""
    
    def __init__(self):
        self.simulation_models = {
            "physics": self._physics_simulation,
            "chemistry": self._chemistry_simulation,
            "biology": self._biology_simulation,
            "environmental": self._environmental_simulation,
            "engineering": self._engineering_simulation,
            "medicine": self._medicine_simulation,
            "general": self._general_simulation
        }
        
        # Simulation parameters for different domains
        self.domain_configs = {
            "physics": {
                "noise_level": 0.02,
                "precision": 0.001,
                "time_scales": "seconds to hours"
            },
            "chemistry": {
                "noise_level": 0.05,
                "precision": 0.01,
                "time_scales": "minutes to days"
            },
            "biology": {
                "noise_level": 0.15,
                "precision": 0.1,
                "time_scales": "hours to months"
            },
            "environmental": {
                "noise_level": 0.10,
                "precision": 0.05,
                "time_scales": "days to years"
            }
        }

    def run_experiment(self, domain: str, parameters: Dict[str, Any], 
                      measurements: List[str]) -> Dict[str, List[float]]:
        """Run domain-specific simulation experiment"""
        
        print(f"🔧 Running {domain} simulation...")
        simulator_func = self.simulation_models.get(domain, self._general_simulation)
        
        try:
            results = simulator_func(parameters, measurements)
            print(f"✅ {domain} simulation completed successfully")
            return results
        except Exception as e:
            print(f"❌ Simulation error: {str(e)}")
            return self._fallback_simulation(parameters, measurements)

    def _physics_simulation(self, parameters: Dict[str, Any], measurements: List[str]) -> Dict[str, List[float]]:
        """Physics domain simulation with realistic models"""
        results = {}
        
        # Temperature effects simulation
        if "temperature" in parameters:
            temp_range = parameters["temperature"]
            results["temperature_levels"] = temp_range
            results["response_values"] = []
            
            for temp in temp_range:
                # Generic temperature-dependent response (thermal expansion, resistance, etc.)
                base_response = 100
                # Arrhenius-like temperature dependence
                temp_effect = math.exp(-1000 / (8.314 * (temp + 273.15)))
                noise = random.gauss(0, self.domain_configs["physics"]["noise_level"])
                response = base_response * temp_effect * (1 + noise)
                results["response_values"].append(max(0, response))
        
        # Force and motion simulations
        if "force" in str(measurements).lower() or "motion" in str(measurements).lower():
            time_points = np.linspace(0, parameters.get("time_duration", 10), 100)
            results["time_data"] = time_points.tolist()
            
            # Harmonic motion with damping
            frequency = parameters.get("frequency", 1.0)
            damping = parameters.get("damping", 0.1)
            results["displacement"] = [
                math.exp(-damping * t) * math.cos(2 * math.pi * frequency * t) + random.gauss(0, 0.01)
                for t in time_points
            ]
            
            # Velocity (derivative)
            results["velocity"] = [
                -damping * math.exp(-damping * t) * math.cos(2 * math.pi * frequency * t) 
                - 2 * math.pi * frequency * math.exp(-damping * t) * math.sin(2 * math.pi * frequency * t)
                + random.gauss(0, 0.05)
                for t in time_points
            ]
        
        return results

    def _chemistry_simulation(self, parameters: Dict[str, Any], measurements: List[str]) -> Dict[str, List[float]]:
        """Chemistry domain simulation with kinetics models"""
        results = {}
        
        # Concentration effects
        if "concentration" in parameters:
            conc_range = parameters["concentration"]
            results["concentration_levels"] = conc_range
            results["reaction_rates"] = []
            
            for conc in conc_range:
                # Power law kinetics: rate = k * [A]^n
                rate_constant = 0.1
                reaction_order = parameters.get("reaction_order", 1.5)
                base_rate = rate_constant * (conc ** reaction_order)
                noise = random.gauss(0, self.domain_configs["chemistry"]["noise_level"])
                rate = base_rate * (1 + noise)
                results["reaction_rates"].append(max(0, rate))
        
        # Temperature effects on rate (Arrhenius equation)
        if "temperature" in parameters:
            temp_range = parameters["temperature"]
            results["temperature_celsius"] = temp_range
            results["rate_constants"] = []
            
            A = 1e6  # pre-exponential factor
            Ea = 50000  # activation energy (J/mol)
            R = 8.314  # gas constant
            
            for temp in temp_range:
                temp_k = temp + 273.15
                k = A * math.exp(-Ea / (R * temp_k))
                noise = random.gauss(0, 0.03)
                results["rate_constants"].append(k * (1 + noise))
        
        # pH effects
        if "pH" in parameters:
            pH_range = parameters["pH"]
            results["pH_levels"] = pH_range
            results["activity_coefficients"] = []
            
            for ph in pH_range:
                # Bell-shaped pH response (enzyme-like)
                optimal_ph = 7.0
                activity = math.exp(-0.5 * ((ph - optimal_ph) / 1.5) ** 2)
                noise = random.gauss(0, 0.04)
                results["activity_coefficients"].append(max(0, activity * (1 + noise)))
        
        return results

    def _biology_simulation(self, parameters: Dict[str, Any], measurements: List[str]) -> Dict[str, List[float]]:
        """Biology domain simulation with population and growth models"""
        results = {}
        
        # Light intensity effects on photosynthesis/growth
        if "light_intensity" in parameters:
            light_range = parameters["light_intensity"]
            results["light_levels_lux"] = light_range
            results["photosynthesis_rate"] = []
            
            for light in light_range:
                # Michaelis-Menten kinetics for light saturation
                vmax = 50  # maximum rate
                km = 200   # half-saturation constant
                rate = (vmax * light) / (km + light)
                noise = random.gauss(0, self.domain_configs["biology"]["noise_level"])
                results["photosynthesis_rate"].append(max(0, rate * (1 + noise)))
        
        # Nutrient concentration effects
        if "nutrient_concentration" in parameters:
            nutrient_range = parameters["nutrient_concentration"]
            results["nutrient_levels"] = nutrient_range
            results["growth_rates"] = []
            
            for nutrient in nutrient_range:
                # Liebig's law of minimum - limiting nutrient
                max_growth = 15
                growth = max_growth * (nutrient / (1 + nutrient))  # saturation curve
                noise = random.gauss(0, 0.2)
                results["growth_rates"].append(max(0, growth + noise))
        
        # Population dynamics over time
        if "observation_period" in parameters:
            time_hours = np.linspace(0, parameters["observation_period"], 50)
            results["time_hours"] = time_hours.tolist()
            
            # Logistic growth with environmental stochasticity
            K = 1000  # carrying capacity
            N0 = 50   # initial population
            r = 0.05  # intrinsic growth rate
            
            results["population_size"] = []
            for t in time_hours:
                # Logistic growth with noise
                N = K / (1 + ((K - N0) / N0) * math.exp(-r * t))
                stochastic_factor = random.gauss(1, 0.1)  # 10% environmental variability
                population = N * stochastic_factor
                results["population_size"].append(max(1, population))
        
        return results

    def _environmental_simulation(self, parameters: Dict[str, Any], measurements: List[str]) -> Dict[str, List[float]]:
        """Environmental science simulation"""
        results = {}
        
        # Pollution and air quality
        if "air_quality_index" in parameters:
            aqi_range = parameters["air_quality_index"]
            results["air_quality_index"] = aqi_range
            results["health_impact_score"] = []
            
            for aqi in aqi_range:
                # Non-linear health impact
                impact = 100 * (1 - math.exp(-aqi / 150))
                noise = random.gauss(0, self.domain_configs["environmental"]["noise_level"])
                results["health_impact_score"].append(max(0, impact * (1 + noise)))
        
        # Climate effects
        if "humidity" in parameters:
            humidity_range = parameters["humidity"]
            results["humidity_percent"] = humidity_range
            results["ecosystem_response"] = []
            
            for humidity in humidity_range:
                # Optimal humidity response curve
                optimal_humidity = 60
                response = 100 * math.exp(-0.01 * (humidity - optimal_humidity) ** 2)
                seasonal_variation = 10 * math.sin(humidity * 0.1)
                noise = random.gauss(0, 5)
                total_response = response + seasonal_variation + noise
                results["ecosystem_response"].append(max(0, total_response))
        
        # Carbon cycle simulation
        if "carbon_concentration" in parameters:
            co2_range = parameters.get("carbon_concentration", [350, 400, 450, 500, 550])
            results["co2_ppm"] = co2_range
            results["temperature_anomaly"] = []
            
            for co2 in co2_range:
                # Logarithmic relationship (simplified climate sensitivity)
                baseline_co2 = 350
                climate_sensitivity = 3.0  # degrees per CO2 doubling
                temp_anomaly = climate_sensitivity * math.log(co2 / baseline_co2) / math.log(2)
                noise = random.gauss(0, 0.2)
                results["temperature_anomaly"].append(temp_anomaly + noise)
        
        return results

    def _engineering_simulation(self, parameters: Dict[str, Any], measurements: List[str]) -> Dict[str, List[float]]:
        """Engineering domain simulation"""
        results = {}
        
        # Material properties
        if "stress" in str(measurements).lower() or "strain" in str(measurements).lower():
            stress_range = parameters.get("applied_stress", [0, 10, 20, 30, 40, 50])
            results["stress_mpa"] = stress_range
            results["strain_percent"] = []
            
            # Hooke's law with yield point
            elastic_modulus = 200000  # MPa (steel-like)
            yield_strength = 250      # MPa
            
            for stress in stress_range:
                if stress <= yield_strength:
                    strain = (stress / elastic_modulus) * 100  # convert to percentage
                else:
                    # Plastic deformation
                    elastic_strain = (yield_strength / elastic_modulus) * 100
                    plastic_strain = (stress - yield_strength) * 0.001
                    strain = elastic_strain + plastic_strain
                
                noise = random.gauss(0, 0.02)
                results["strain_percent"].append(max(0, strain * (1 + noise)))
        
        # Efficiency simulations
        if "efficiency" in str(measurements).lower():
            input_range = parameters.get("input_power", [100, 200, 300, 400, 500])
            results["input_power_watts"] = input_range
            results["efficiency_percent"] = []
            
            for power in input_range:
                # Efficiency curve with optimal operating point
                optimal_power = 300
                max_efficiency = 85
                efficiency = max_efficiency * math.exp(-0.000005 * (power - optimal_power) ** 2)
                noise = random.gauss(0, 1.5)
                results["efficiency_percent"].append(max(0, min(100, efficiency + noise)))
        
        return results

    def _medicine_simulation(self, parameters: Dict[str, Any], measurements: List[str]) -> Dict[str, List[float]]:
        """Medical/pharmaceutical simulation"""
        results = {}
        
        # Drug dosage effects
        if "dosage" in parameters or "dose" in parameters:
            dose_range = parameters.get("dosage", parameters.get("dose", [0, 5, 10, 15, 20]))
            results["dosage_mg"] = dose_range
            results["therapeutic_response"] = []
            
            for dose in dose_range:
                # Hill equation for drug response
                max_response = 100
                EC50 = 10  # half-maximal effective concentration
                hill_coefficient = 2
                
                response = (max_response * (dose ** hill_coefficient)) / (EC50 ** hill_coefficient + dose ** hill_coefficient)
                noise = random.gauss(0, 5)  # biological variability
                results["therapeutic_response"].append(max(0, response + noise))
        
        # Time-course pharmacokinetics
        if "time_course" in str(measurements).lower():
            time_hours = np.linspace(0, 24, 48)
            results["time_hours"] = time_hours.tolist()
            
            # Single compartment pharmacokinetic model
            dose = parameters.get("initial_dose", 100)
            elimination_rate = 0.1  # per hour
            
            results["plasma_concentration"] = [
                dose * math.exp(-elimination_rate * t) + random.gauss(0, 2)
                for t in time_hours
            ]
        
        return results

    def _general_simulation(self, parameters: Dict[str, Any], measurements: List[str]) -> Dict[str, List[float]]:
        """General simulation for unknown or mixed domains"""
        results = {}
        
        # Find the first list parameter as independent variable
        independent_var = None
        independent_key = None
        
        for key, value in parameters.items():
            if isinstance(value, list) and all(isinstance(x, (int, float)) for x in value):
                independent_var = value
                independent_key = key
                break
        
        if not independent_var:
            # Create default parameter range
            independent_var = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            independent_key = "parameter_levels"
        
        results[independent_key] = independent_var
        
        # Generate multiple dependent variables with different relationships
        
        # Linear relationship
        results["linear_response"] = [
            10 + 5 * x + random.gauss(0, 1) for x in independent_var
        ]
        
        # Exponential relationship
        results["exponential_response"] = [
            50 * (1 - math.exp(-0.3 * x)) + random.gauss(0, 2) for x in independent_var
        ]
        
        # Polynomial relationship
        results["polynomial_response"] = [
            20 + 3 * x - 0.1 * x**2 + random.gauss(0, 1.5) for x in independent_var
        ]
        
        # Logarithmic relationship
        results["logarithmic_response"] = [
            30 * math.log(x + 1) + random.gauss(0, 1) for x in independent_var
        ]
        
        # Select most appropriate response based on measurements
        primary_response = "linear_response"
        if "growth" in str(measurements).lower():
            primary_response = "exponential_response"
        elif "saturation" in str(measurements).lower():
            primary_response = "logarithmic_response"
        elif "optimization" in str(measurements).lower():
            primary_response = "polynomial_response"
        
        # Rename primary response to generic name
        results["measured_response"] = results[primary_response]
        
        return results

    def _fallback_simulation(self, parameters: Dict[str, Any], measurements: List[str]) -> Dict[str, List[float]]:
        """Fallback simulation when domain-specific simulation fails"""
        return {
            "parameter_values": [1, 2, 3, 4, 5],
            "measured_response": [10, 15, 22, 28, 35],
            "measurement_error": [0.5, 0.7, 1.0, 0.8, 1.2]
        }

class PendulumSimulator:
    """Specialized pendulum physics simulation (kept for backward compatibility)"""
    
    def __init__(self, length: float = 1.0, gravity: float = 9.81):
        self.length = length
        self.gravity = gravity
        
    def simulate(self, initial_angle: float, time_steps: int = 1000, 
                dt: float = 0.01, damping: float = 0.01) -> Tuple[List[float], List[float]]:
        """Simulate pendulum motion with damping"""
        times = []
        angles = []
        
        theta = initial_angle
        omega = 0.0
        
        for i in range(time_steps):
            time = i * dt
            times.append(time)
            angles.append(theta)
            
            alpha = -(self.gravity / self.length) * math.sin(theta) - 2 * damping * omega
            omega += alpha * dt
            theta += omega * dt
            
        return times, angles
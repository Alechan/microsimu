import re
from api.std_lib.lawm.regions import DEFAULT_REGIONS

hardcoded_params = {
    "IAID": "F",
    "IPRIN": "0",
    "NHIST": 0,
    "TRAID": 2.0000000E-02,
}


class LAWMFortranCFGFormatter:
    def cfg_content_from_validated_data(self, validated_data):
        params_flattened = self.flatten_params(validated_data)
        final_params = params_flattened | hardcoded_params
        final_str        = self.to_final_str(final_params)
        return final_str

    def flatten_params(self, validated_data):
        reg_params_flattened = self.flatten_regional_params(validated_data)
        gen_params_flattened = self.flatten_general_params(validated_data)
        params_flattened = gen_params_flattened | reg_params_flattened
        return params_flattened

    def flatten_regional_params(self, validated_data):
        lvl_1 = self.flatten_regional_params_lvl_1(validated_data)
        lvl_2 = self.flatten_regional_params_lvl_2(lvl_1)
        return lvl_2

    def flatten_general_params(self, validated_data):
        lvl_1 = self.flatten_general_params_lvl_1(validated_data)
        lvl_2 = self.flatten_general_params_lvl_2(lvl_1)
        return lvl_2

    def flatten_regional_params_lvl_1(self, validated_data):
        """
        From {regional_params:[{param:ParamValue)}]} to {fortran_name:{region_name:value}}
        """
        all_reg_params = validated_data["regional_parameters"]
        flattened_reg_params = {}
        for reg_param in all_reg_params:
            region_name = reg_param["region"].name
            params = reg_param.keys() - {"region"}
            for p in params:
                fortran_name = reg_param[p].fortran_name
                value = reg_param[p].value
                if fortran_name in flattened_reg_params:
                    flattened_param_values = flattened_reg_params[fortran_name]
                    flattened_param_values[region_name] = value
                else:
                    flattened_reg_params[fortran_name] = {region_name: value}
        return flattened_reg_params

    def flatten_regional_params_lvl_2(self, flattened_lvl_1):
        """
        From {fortran_name_1: {region_name: value}, fortran_name_2: {region_name: value}, ...}
        to {fortran_name: [value]}
        """
        flattened_lvl_2_gamma = self.get_lvl_2_gamma_params(flattened_lvl_1)
        flattened_lvl_2_non_gamma = self.get_lvl_2_flattend_non_gamma_params(flattened_lvl_1)
        return flattened_lvl_2_gamma | flattened_lvl_2_non_gamma

    def get_lvl_2_flattend_non_gamma_params(self, flattened_lvl_1):
        non_gamma_param_keys = [x for x in flattened_lvl_1.keys() if "GAMMA" not in x]
        flattened_lvl_2_non_gamma = {self.get_base_fortran_name(param_name): [] for param_name in non_gamma_param_keys}
        for region in DEFAULT_REGIONS:
            region_param_values = []
            for param_name in non_gamma_param_keys:
                value = flattened_lvl_1[param_name][region.name]
                region_param_values.append(value)
                base_fortran_name = self.get_base_fortran_name(param_name)
                flattened_lvl_2_non_gamma[base_fortran_name].append(value)
        return flattened_lvl_2_non_gamma

    def get_lvl_2_gamma_params(self, flattened_lvl_1):
        """
        Among the regional params, GAMMA is the only one that was split in different self contained
        parameters, so it's the only one that we have to flatten
        """
        gamma_param_keys = sorted([x for x in flattened_lvl_1.keys() if "GAMMA" in x])
        flattened_lvl_2 = {"GAMMA": []}
        for region in DEFAULT_REGIONS:
            region_gamma_lists = []
            for sub_gamma in gamma_param_keys:
                sub_gamma_value = flattened_lvl_1[sub_gamma][region.name]
                region_gamma_lists.append(sub_gamma_value)
            flattened_lvl_2["GAMMA"].append(region_gamma_lists)
        return flattened_lvl_2

    def flatten_general_params_lvl_1(self, validated_data):
        """
        From {general_parameters:{param:ParamValue)}} to {fortran_name:value}
        """
        gen_params = validated_data["general_parameters"]
        flattened_gen_params = {}
        for k, v in gen_params.items():
            fortran_name = v.fortran_name
            value = v.value
            flattened_gen_params[fortran_name] = value
        return flattened_gen_params

    def flatten_general_params_lvl_2(self, flattened_lvl_1):
        flattened_lvl_2_wth = self.get_flattened_lvl_2_wth_params(flattened_lvl_1)
        flattened_lvl_2_non_wth = {k: v for k, v in flattened_lvl_1.items() if "WTH" not in k}
        return flattened_lvl_2_wth | flattened_lvl_2_non_wth

    def get_flattened_lvl_2_wth_params(self, flattened_lvl_1):
        n_repeated_var = 26
        wth_param_keys = [f"WTH({i})" for i in range(1, n_repeated_var + 1)]
        joined_wth_values = []
        for sub_wth in wth_param_keys:
            sub_wth_value = flattened_lvl_1[sub_wth]
            joined_wth_values.append(sub_wth_value)
        # Add 4 "irrelevant" values because the fortran version expects them
        joined_wth_values = joined_wth_values + [-1 for i in range(4)]
        flattened_lvl_2 = {"WTH": joined_wth_values}
        return flattened_lvl_2

    def get_base_fortran_name(self, fortran_name):
        base_fortran_name = re.sub(r"\(.*$", "", fortran_name)
        return base_fortran_name

    def to_final_str(self, final_dict):
        final_str_per_line = []
        sorted_param_names = sorted(final_dict.keys())
        for p_name in sorted_param_names:
            final_str_per_line.append(p_name)
            p_val = final_dict[p_name]
            # Quick and dirty, just how I like it
            if isinstance(p_val, list):
                if isinstance(p_val[0], list):
                    # p_val is a list of lists
                    for sublist in p_val:
                        values_as_str = [str(x) for x in sublist]
                        val_line = " ".join(values_as_str)
                        final_str_per_line.append(val_line)
                else:
                    # p_val is a list of values
                    lines_as_str = [[str(x) for x in p_val[i:i+5]] for i in range(0,len(p_val), 5)]
                    for values_as_str in lines_as_str:
                        val_line = " ".join(values_as_str)
                        final_str_per_line.append(val_line)
            else:
                # p_val is a lone value
                value_as_str = str(p_val)
                final_str_per_line.append(value_as_str)
        final_str = "\n".join(final_str_per_line)
        final_str = final_str + "\n"
        return final_str

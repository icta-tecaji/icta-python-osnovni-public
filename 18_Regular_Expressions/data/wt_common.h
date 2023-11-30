#ifndef _WT_COMMON_H_
#define _WT_COMMON_H_
#include "types.h"

#ifdef __cplusplus
extern "C" {
#endif

#define WT_COMMON_VARIANT_CODE 0x01000000

#define WT_COMMON_CUSTOMER_SOFTWARE_VERSION "RE TEST"

#define WT_COMMON_EXCEL_FILENAME "c296d34d-1562-415a-bf89-ae0831ecd96d"


typedef struct
{
	uint8_t wt_major;
	uint8_t wt_minor;
	uint8_t wt_build;
} wt_common_version_param_t;

#define WT_COMMON_VERSION_PARAM_DESC \
{ \
	0, 4, 6 \
}

extern const wt_common_version_param_t WT_COMMON_VERSION_PARAM;

typedef struct
{
	uint8_t pu_major;
	uint8_t pu_minor;
	uint8_t pu_build;
} wt_common_pu_version_param_t;

#define WT_COMMON_PU_VERSION_PARAM_DESC \
{ \
	2, 0, 3 \
}

extern const wt_common_pu_version_param_t WT_COMMON_PU_VERSION_PARAM;

typedef struct
{
	uint8_t min_major;
	uint8_t min_minor;
	uint8_t min_build;
	uint8_t max_major;
	uint8_t max_minor;
	uint8_t max_build;
} wt_common_pu_version_compatibility_param_t;

#define WT_COMMON_PU_VERSION_COMPATIBILITY_PARAM_DESC \
{ \
	2, 0, 3, 255, 255, 255 \
}

extern const wt_common_pu_version_compatibility_param_t WT_COMMON_PU_VERSION_COMPATIBILITY_PARAM;

typedef struct
{
	uint8_t min_major;
	uint8_t min_minor;
	uint8_t min_build;
	uint8_t max_major;
	uint8_t max_minor;
	uint8_t max_build;
} wt_common_mu_version_compatibility_param_t;

#define WT_COMMON_MU_VERSION_COMPATIBILITY_PARAM_DESC \
{ \
	2, 4, 39, 3, 4, 255 \
}

extern const wt_common_mu_version_compatibility_param_t WT_COMMON_MU_VERSION_COMPATIBILITY_PARAM;

typedef struct
{
	uint8_t min_major;
	uint8_t min_minor;
	uint8_t min_build;
	uint8_t max_major;
	uint8_t max_minor;
	uint8_t max_build;
} wt_common_ui_version_compatibility_param_t;

#define WT_COMMON_UI_VERSION_COMPATIBILITY_PARAM_DESC \
{ \
	2, 0, 3, 2, 255, 255 \
}

extern const wt_common_ui_version_compatibility_param_t WT_COMMON_UI_VERSION_COMPATIBILITY_PARAM;

typedef struct
{
	uint16_t number_of_program_repeats;
	uint16_t pause_between_programs_in_sec;
} wt_common_debug_param_t;

#define WT_COMMON_DEBUG_PARAM_DESC \
{ \
	0, 10 \
}

extern const wt_common_debug_param_t WT_COMMON_DEBUG_PARAM;

typedef struct
{
	uint8_t port;
	bool disable;
} wt_trace_config_param_t;

#define WT_TRACE_CONFIG_PARAM_DESC \
{ \
	5, 0 \
}

extern const wt_trace_config_param_t WT_TRACE_CONFIG_PARAM;

typedef struct
{
	uint8_t drum_type : 4;
	uint8_t max_spin : 4;
	uint8_t motor : 3;
	uint8_t mu_config : 5;
	float zero_inertia_low;
	float zero_inertia_high;
	float zero_inertia_high_4_turns;
	float zero_unbalance_low;
	float zero_unbalance_high;
	float mwc_inter_x0;
	float mwc_inter_x1;
	float mwc_inter_x2;
	float mwc_inter_x3;
	float mwc_inter_x4;
	uint16_t mwc_inter_y0;
	uint16_t mwc_inter_y1;
	uint16_t mwc_inter_y2;
	uint16_t mwc_inter_y3;
	uint16_t mwc_inter_y4;
	uint8_t production_test_number;
	float AuBallLimitLow;
	float AuBallLimitHigh;
} wt_common_dams_param_t;

#define WT_COMMON_DAMS_PARAM_DESC \
{ \
	{ \
		WT_DRUM_TYPE_68L_10kg, WT_SPIN_1600, WT_MOTOR_KING3, WT_MU_MACHINE_TYPE_1_838535, 0.008182636, 0.010502395, 0.01068, 0.004399234, 0.005140646, 0, 0.00283, 0.00442, 0.00586, 0.00841, 0, 2000, 4000, 6000, 10000, 33, 0.1, 0.1 \
	} \
}

extern const wt_common_dams_param_t WT_COMMON_DAMS_PARAM[1];

typedef struct
{
	uint8_t total_percent;
	uint8_t additional_time;
} wt_common_tte_time_limit_param_t;

#define WT_COMMON_TTE_TIME_LIMIT_PARAM_DESC \
{ \
	20, 120 \
}

extern const wt_common_tte_time_limit_param_t WT_COMMON_TTE_TIME_LIMIT_PARAM;

typedef struct
{
	uint16_t enable : 1;
	uint16_t detect_time : 7;
	uint16_t detect_level : 8;
} wt_common_foam_detection_param_t;

#define WT_COMMON_FOAM_DETECTION_PARAM_DESC \
{ \
	1, 60, 30 \
}

extern const wt_common_foam_detection_param_t WT_COMMON_FOAM_DETECTION_PARAM;

typedef struct
{
	uint8_t trial_counter : 3;
	uint8_t wait_time : 5;
	uint8_t fill_time;
	uint8_t drain_time;
} wt_common_antifoam_intermediate_param_t;

#define WT_COMMON_ANTIFOAM_INTERMEDIATE_PARAM_DESC \
{ \
	2, 10, 60, 60 \
}

extern const wt_common_antifoam_intermediate_param_t WT_COMMON_ANTIFOAM_INTERMEDIATE_PARAM;

typedef struct
{
	uint32_t drain_time : 7;
	uint32_t trial_max : 5;
	uint32_t recirculation_time : 5;
	uint32_t repeated_spin_max : 3;
	uint32_t unremoved_foam_counter_max : 3;
	uint32_t second_drain_time : 9;
} wt_common_antifoam_final_param_t;

#define WT_COMMON_ANTIFOAM_FINAL_PARAM_DESC \
{ \
	60, 7, 10, 3, 1, 240 \
}

extern const wt_common_antifoam_final_param_t WT_COMMON_ANTIFOAM_FINAL_PARAM;

typedef struct
{
	uint8_t max_cycles;
	uint8_t max_alert;
} wt_common_steril_tub_alert_param_t;

#define WT_COMMON_STERIL_TUB_ALERT_PARAM_DESC \
{ \
	40, 6 \
}

extern const wt_common_steril_tub_alert_param_t WT_COMMON_STERIL_TUB_ALERT_PARAM;

typedef struct
{
	uint16_t lock_t1;
	uint16_t lock_t2;
	uint16_t unlock_t1;
	uint16_t unlock_t2;
	uint16_t unlock_t3;
} wt_common_door_lock_param_t;

#define WT_COMMON_DOOR_LOCK_PARAM_DESC \
{ \
	2500, 5000, 500, 5000, 6500 \
}

extern const wt_common_door_lock_param_t WT_COMMON_DOOR_LOCK_PARAM;

#ifdef __cplusplus
}
#endif

#endif

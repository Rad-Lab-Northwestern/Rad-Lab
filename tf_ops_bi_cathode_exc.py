from pathlib import Path
import math
import csv

# =========================
# User-adjustable parameters
# =========================


# Main Google Drive archive root
ARCHIVE_ROOT_DIR = Path("/Users/fuchang/Desktop/Google Drive/TF_Project_Archive")

# Archive hierarchy
PROGRAM_FOLDER = "01_AIMDs" # DO NOT CHANGE
AIMD_TYPE_FOLDER = "CIED"  # e.g. CIED, DBS, SCS, VNS, etc.
LEAD_MODEL_MANUFACTURER_LENGTH_FOLDER = "Lead_MDT_4968_25cm" # Need to follow the format: Lead_manufacturer_model_length
TERMINATION_CONDITION_FOLDER = "Full_system" # Need to follow the format: Abandoned_Capped, Abandoned_Uncapped, Full_system, etc.
IPG_MODEL_FOLDER = "IPG_MDT_azure_xt_dr" # Need to follow the format: IPG_manufacturer_model
FIELD_STRENGTH_FOLDER = "64MHz_1p5T" # Need to follow the format: frequency_field_strength, e.g. 23p6MHz_0.55T, 64MHz_1.5T, 127MHz_3T
DATA_TYPE_FOLDER = "01_TF"  # DO NOT CHANGE
RUN_FOLDER = "2026-04-24_run01_FJ"  # Need to follow the format: YYY-MM-DD_run##_initials

# Short identifiers used only in output filenames
FILENAME_LEAD_LABEL = LEAD_MODEL_MANUFACTURER_LENGTH_FOLDER
FILENAME_IPG_LABEL = IPG_MODEL_FOLDER
# FILENAME_IPG_LABEL = TERMINATION_CONDITION_FOLDER  # If the IPG model is not available, use the termination condition folder instead

# Keep only the run number portion for filenames, e.g. "run01" from RUN_FOLDER
# This is used for the output filenames
# No need to change this.
RUN_NUMBER_LABEL = next(
    (part for part in RUN_FOLDER.split("_") if part.lower().startswith("run")),
    RUN_FOLDER,
)

# Folder names inside one run. DO NOT CHANGE THIS.
FORM_FOLDER = "01_form"
RAW_FOLDER = "02_raw"
RAW_PROCESSED_FOLDER = "03_raw_processed"
INTERP_EXTRAP_FOLDER = "04_interpolated_extrapolated"
PLOTS_FOLDER = "05_plots"

# Branch folder names expected by this script. DO NOT CHANGE THIS.
ANODE_BRANCH_FOLDER = "cathode_exc_anode_branch"
CATHODE_BRANCH_FOLDER = "cathode_exc_cathode_branch"
SHARED_BRANCH_FOLDER = "cathode_exc_shared_branch"

# Build the full run root under the archive. DO NOT CHANGE THIS.
RUN_ROOT_DIR = (
    ARCHIVE_ROOT_DIR
    / PROGRAM_FOLDER
    / AIMD_TYPE_FOLDER
    / LEAD_MODEL_MANUFACTURER_LENGTH_FOLDER
    / TERMINATION_CONDITION_FOLDER
    / IPG_MODEL_FOLDER
    / FIELD_STRENGTH_FOLDER
    / DATA_TYPE_FOLDER
    / RUN_FOLDER
)

# Run-level folders. DO NOT CHANGE THIS.
FORM_OUTPUT_DIR = RUN_ROOT_DIR / FORM_FOLDER
RAW_OUTPUT_DIR = RUN_ROOT_DIR / RAW_FOLDER
RAW_PROCESSED_OUTPUT_DIR = RUN_ROOT_DIR / RAW_PROCESSED_FOLDER
INTERP_EXTRAP_OUTPUT_DIR = RUN_ROOT_DIR / INTERP_EXTRAP_FOLDER
PLOT_OUTPUT_DIR = RUN_ROOT_DIR / PLOTS_FOLDER

# Raw input branch folders used by the analysis. DO NOT CHANGE THIS.
ANODE_RAW_DIR = RAW_OUTPUT_DIR / ANODE_BRANCH_FOLDER
CATHODE_RAW_DIR = RAW_OUTPUT_DIR / CATHODE_BRANCH_FOLDER
SHARED_RAW_DIR = RAW_OUTPUT_DIR / SHARED_BRANCH_FOLDER

# Base input folder for the existing analysis logic. DO NOT CHANGE THIS.
TF_INTERP_EXT_DIR = RAW_OUTPUT_DIR

# Frequency to extract from each .S2P file.
TARGET_FREQ = 64000000.000  # Need to copy and paste the frequency you want to extract from the .S2P file
# TARGET_FREQ = 23600000.000

# Distance settings (mm)
TOTAL_LEAD_LENGTH_MM = 250  # Need to change this if the lead length is different from the default value
BIFURCATION_START_MM = 100 # Need to change this if the bifurcation start is different from the default value
INTERP_STEP_MM = 5  # Need to change this if the interpolation step is different from the default value

#######################################################################################


def get_or_create_dir(folder_path: Path, folder_label: str) -> Path:
    """Create a folder if it does not exist yet, otherwise reuse the existing folder."""
    if folder_path.is_dir():
        print(f"Using existing {folder_label}: {folder_path}")
        return folder_path

    folder_path.mkdir(parents=True, exist_ok=True)
    print(f"Created {folder_label}: {folder_path}")
    return folder_path


def create_run_folder_tree() -> None:
    """Create the standard folder tree for one archive run, including raw branch folders."""
    print("\n=== Creating / checking run folder tree ===")
    get_or_create_dir(RUN_ROOT_DIR, "run root folder")
    get_or_create_dir(FORM_OUTPUT_DIR, "form folder")
    get_or_create_dir(RAW_OUTPUT_DIR, "raw data folder")
    get_or_create_dir(RAW_PROCESSED_OUTPUT_DIR, "raw processed folder")
    get_or_create_dir(INTERP_EXTRAP_OUTPUT_DIR, "interpolated/extrapolated folder")
    get_or_create_dir(PLOT_OUTPUT_DIR, "plot folder")

    # Raw branch folders expected by this script
    get_or_create_dir(ANODE_RAW_DIR, "cathode excitation anode-branch raw folder")
    get_or_create_dir(CATHODE_RAW_DIR, "cathode excitation cathode-branch raw folder")
    get_or_create_dir(SHARED_RAW_DIR, "cathode excitation shared-branch raw folder")


def prompt_user_to_place_raw_files() -> None:
    """Pause so the user can copy raw .S2P files into the correct raw branch folders."""
    print("\n=== Raw data upload step ===")
    print("Please place the raw .S2P files into these folders:")
    print(f"  {ANODE_RAW_DIR}")
    print(f"  {CATHODE_RAW_DIR}")
    print(f"  {SHARED_RAW_DIR}")
    print("\nExpected layout:")
    print(f"  {ANODE_RAW_DIR}/*.S2P")
    print(f"  {CATHODE_RAW_DIR}/*.S2P")
    print(f"  {SHARED_RAW_DIR}/*.S2P")
    input("\nAfter you finish copying the raw files, press Enter to continue...")


def validate_required_raw_data() -> None:
    """Stop the script if any required raw branch folder does not contain .S2P files."""
    print("\n=== Validating raw data folders ===")

    missing_or_empty = []
    for folder in [ANODE_RAW_DIR, CATHODE_RAW_DIR, SHARED_RAW_DIR]:
        s2p_files = list(folder.glob("*.S2P"))
        if not s2p_files:
            missing_or_empty.append(folder)
        else:
            print(f"Found {len(s2p_files)} .S2P files in: {folder}")

    if missing_or_empty:
        print("\n[ERROR] These required raw folders are empty or missing .S2P files:")
        for folder in missing_or_empty:
            print(f"  {folder}")
        raise SystemExit(
            "\nStopping because required raw files were not found in all branch folders."
        )

    print("Raw data check passed. Analysis will start.")


def sanitize_filename_part(text: str) -> str:
    """Convert a metadata string into a filesystem-friendly filename part."""
    safe = text.strip().replace(" ", "_")
    safe = safe.replace("/", "-").replace("\\", "-")
    safe = safe.replace(":", "-").replace(",", "_")
    return safe


def format_frequency_token(target_freq: float) -> str:
    """Convert a frequency in Hz to a readable filename token."""
    mhz = target_freq / 1_000_000.0
    return f"{mhz:.3f}MHz".replace(".", "p")


def build_output_stem(target_freq: float) -> str:
    """Build a short filename stem using lead, IPG, frequency, and run number only."""
    parts = [
        FILENAME_LEAD_LABEL,
        FILENAME_IPG_LABEL,
        format_frequency_token(target_freq),
        RUN_NUMBER_LABEL,
    ]
    return "__".join(sanitize_filename_part(part) for part in parts)


def build_output_filename(label: str, extension: str, target_freq: float) -> str:
    """Build a complete output filename with metadata stem and descriptive label."""
    stem = build_output_stem(target_freq)
    safe_label = sanitize_filename_part(label)
    return f"{stem}__{safe_label}.{extension}"


def extract_distance_to_ipg(file_name: str) -> str:
    """Get distance token from filename, e.g. 035MM from 035MM_745MM.S2P."""
    stem = Path(file_name).stem
    return stem.split("_")[0]


def distance_token_to_mm(distance_token: str) -> float:
    """Convert distance token like 035MM to numeric mm value."""
    return float(distance_token.upper().replace("MM", ""))


def linear_interp_extrap(
    x_src: list[float], y_src: list[float], x_new: list[float]
) -> list[float]:
    """Piecewise-linear interpolation with linear extrapolation at both ends."""
    if len(x_src) < 2:
        raise ValueError("Need at least 2 points for interpolation/extrapolation.")

    pairs = sorted(zip(x_src, y_src), key=lambda p: p[0])
    x_sorted = [p[0] for p in pairs]
    y_sorted = [p[1] for p in pairs]

    out = []
    for x in x_new:
        if x <= x_sorted[0]:
            x0, y0 = x_sorted[0], y_sorted[0]
            x1, y1 = x_sorted[1], y_sorted[1]
        elif x >= x_sorted[-1]:
            x0, y0 = x_sorted[-2], y_sorted[-2]
            x1, y1 = x_sorted[-1], y_sorted[-1]
        else:
            idx = 0
            for j in range(len(x_sorted) - 1):
                if x_sorted[j] <= x <= x_sorted[j + 1]:
                    idx = j
                    break
            x0, y0 = x_sorted[idx], y_sorted[idx]
            x1, y1 = x_sorted[idx + 1], y_sorted[idx + 1]

        if x1 == x0:
            y = y0
        else:
            y = y0 + (x - x0) * (y1 - y0) / (x1 - x0)
        out.append(y)
    return out


def unwrap_phase_with_distance(
    distance_mm: list[float], phase_rad: list[float]
) -> list[float]:
    """Unwrap phase in distance order to avoid -pi/pi interpolation jumps."""
    if not distance_mm:
        return []

    pairs = sorted(zip(distance_mm, phase_rad), key=lambda p: p[0])
    dist_sorted = [p[0] for p in pairs]
    phase_sorted = [p[1] for p in pairs]

    unwrapped_sorted = [phase_sorted[0]]
    for p in phase_sorted[1:]:
        prev = unwrapped_sorted[-1]
        delta = p - prev
        while delta > math.pi:
            p -= 2.0 * math.pi
            delta = p - prev
        while delta < -math.pi:
            p += 2.0 * math.pi
            delta = p - prev
        unwrapped_sorted.append(p)

    # Map back to original input order
    unwrapped_by_dist = {d: p for d, p in zip(dist_sorted, unwrapped_sorted)}
    return [unwrapped_by_dist[d] for d in distance_mm]


def save_current_plot(plt_module, filename: str) -> None:
    """Save the current matplotlib figure into the run plot folder."""
    plot_path = PLOT_OUTPUT_DIR / filename
    plt_module.savefig(plot_path, dpi=300, bbox_inches="tight")
    print(f"Saved plot: {plot_path}")


def save_original_csv_rows(out_csv: Path, rows: list[dict[str, float | str]]) -> None:
    """Save original extracted S21 data rows in series and distance order."""
    sorted_rows = sorted(
        rows,
        key=lambda row: (str(row["series"]), float(row["distance_to_ipg_mm"])),
    )

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "series",
                "source",
                "distance_to_ipg_mm",
                "S21_real",
                "S21_imag",
                "S21_magnitude",
                "S21_phase_rad",
            ]
        )
        for row in sorted_rows:
            writer.writerow(
                [
                    row["series"],
                    row["source"],
                    row["distance_to_ipg_mm"],
                    row["S21_real"],
                    row["S21_imag"],
                    row["S21_magnitude"],
                    row["S21_phase_rad"],
                ]
            )
    print(f"Saved CSV: {out_csv}")


def save_processed_csv_rows(out_csv: Path, rows: list[dict[str, float | str]]) -> None:
    """Save interpolated/extrapolated S21 data rows in series and distance order."""
    sorted_rows = sorted(
        rows,
        key=lambda row: (str(row["series"]), float(row["distance_to_ipg_mm"])),
    )

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "series",
                "distance_to_ipg_mm",
                "S21_real_interp_extrap",
                "S21_imag_interp_extrap",
                "S21_magnitude_interp_extrap",
                "S21_phase_rad_interp_extrap",
            ]
        )
        for row in sorted_rows:
            writer.writerow(
                [
                    row["series"],
                    row["distance_to_ipg_mm"],
                    row["S21_real_interp_extrap"],
                    row["S21_imag_interp_extrap"],
                    row["S21_magnitude_interp_extrap"],
                    row["S21_phase_rad_interp_extrap"],
                ]
            )
    print(f"Saved CSV: {out_csv}")


def extract_s21_at_freq(base_dir: Path, target_freq: float):
    """Extract S21 real/imag values at the target frequency from all .S2P files in a folder."""
    s21_real_col = []
    s21_imag_col = []
    source_files = []

    # Read files in lexical order
    for fp in sorted(base_dir.rglob("*.S2P")):
        found = False
        with fp.open("r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        # First 5 lines are titles, data starts from line 6
        for line in lines[5:]:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 5:
                continue

            freq = float(parts[0])
            if abs(freq - target_freq) < 1e-6:
                s21_real = float(parts[3])  # 4th column
                s21_imag = float(parts[4])  # 5th column

                s21_real_col.append(s21_real)
                s21_imag_col.append(s21_imag)
                source_files.append(fp.name)
                found = True
                break

        if not found:
            print(f"[WARN] No freq={target_freq:.3f} in {fp}")

    return source_files, s21_real_col, s21_imag_col


def run_branch_analysis(branch_dir: Path, target_freq: float):
    """Print per-file S21 values for one branch folder at the target frequency."""
    files, s21_real_col, s21_imag_col = extract_s21_at_freq(branch_dir, target_freq)

    print(f"\n=== {branch_dir.name} ===")
    print("file,distance_to_ipg,S21_real,S21_imag,S21_magnitude,S21_phase_rad")
    for name, r, i in zip(files, s21_real_col, s21_imag_col):
        distance_to_ipg = extract_distance_to_ipg(name)
        magnitude = math.sqrt(r**2 + i**2)
        phase_rad = math.atan2(i, r)
        print(f"{name},{distance_to_ipg},{r},{i},{magnitude},{phase_rad}")


def run_combined_shared_then_cathode(target_freq: float):
    """Run the combined shared->cathode workflow, plus anode overlap, plots, and CSV export."""
    shared_dir = TF_INTERP_EXT_DIR / SHARED_BRANCH_FOLDER
    cathode_dir = TF_INTERP_EXT_DIR / CATHODE_BRANCH_FOLDER

    shared_files, shared_real, shared_imag = extract_s21_at_freq(shared_dir, target_freq)
    cathode_files, cathode_real, cathode_imag = extract_s21_at_freq(cathode_dir, target_freq)

    combined_files = (
        [f"{shared_dir.name}/{name}" for name in shared_files]
        + [f"{cathode_dir.name}/{name}" for name in cathode_files]
    )
    combined_real = shared_real + cathode_real
    combined_imag = shared_imag + cathode_imag
    combined_distance_mm = []
    combined_magnitude = []
    combined_phase = []
    original_rows = []

    print("\n=== combined_s21 (shared -> cathode) ===")
    print("source,distance_to_ipg,S21_real,S21_imag,S21_magnitude,S21_phase_rad")
    for source, r, i in zip(combined_files, combined_real, combined_imag):
        file_name = Path(source).name
        distance_to_ipg = extract_distance_to_ipg(file_name)
        distance_mm = distance_token_to_mm(distance_to_ipg)
        magnitude = math.sqrt(r**2 + i**2)
        phase_rad = math.atan2(i, r)
        print(f"{source},{distance_to_ipg},{r},{i},{magnitude},{phase_rad}")
        combined_distance_mm.append(distance_mm)
        combined_magnitude.append(magnitude)
        combined_phase.append(phase_rad)
        original_rows.append(
            {
                "series": "shared_to_cathode",
                "source": source,
                "distance_to_ipg_mm": distance_mm,
                "S21_real": r,
                "S21_imag": i,
                "S21_magnitude": magnitude,
                "S21_phase_rad": phase_rad,
            }
        )

    # Also prepare anode branch interpolation/extrapolation for overlap.
    anode_dir = TF_INTERP_EXT_DIR / ANODE_BRANCH_FOLDER
    anode_files, anode_real, anode_imag = extract_s21_at_freq(anode_dir, target_freq)
    anode_distance_mm = []
    anode_magnitude = []
    anode_phase = []
    anode_real_raw = []
    anode_imag_raw = []
    for name, r, i in zip(anode_files, anode_real, anode_imag):
        distance_to_ipg = extract_distance_to_ipg(name)
        distance_mm = distance_token_to_mm(distance_to_ipg)
        anode_distance_mm.append(distance_mm)
        anode_real_raw.append(r)
        anode_imag_raw.append(i)
        magnitude = math.sqrt(r**2 + i**2)
        phase_rad = math.atan2(i, r)
        anode_magnitude.append(magnitude)
        anode_phase.append(phase_rad)
        original_rows.append(
            {
                "series": "anode",
                "source": f"{anode_dir.name}/{name}",
                "distance_to_ipg_mm": distance_mm,
                "S21_real": r,
                "S21_imag": i,
                "S21_magnitude": magnitude,
                "S21_phase_rad": phase_rad,
            }
        )

    try:
        import matplotlib.pyplot as plt  # pyright: ignore[reportMissingImports]
    except ImportError:
        print("[WARN] matplotlib is not installed, skipping scatter plot.")
        return

    # Figure 1: S21 real with original and interpolated/extrapolated data.
    x_line_combined = [
        float(x) for x in range(0, TOTAL_LEAD_LENGTH_MM + 1, INTERP_STEP_MM)
    ]
    y_real_combined = linear_interp_extrap(
        combined_distance_mm, combined_real, x_line_combined
    )
    y_imag_combined = linear_interp_extrap(
        combined_distance_mm, combined_imag, x_line_combined
    )

    x_line_anode = [
        float(x)
        for x in range(BIFURCATION_START_MM, TOTAL_LEAD_LENGTH_MM + 1, INTERP_STEP_MM)
    ]
    y_real_anode = linear_interp_extrap(
        anode_distance_mm, anode_real_raw, x_line_anode
    )
    y_imag_anode = linear_interp_extrap(
        anode_distance_mm, anode_imag_raw, x_line_anode
    )

    plt.figure(figsize=(8, 5))
    plt.scatter(
        combined_distance_mm,
        combined_real,
        alpha=0.9,
        color="#1f77b4",
        label="Combined original S21 real",
    )
    plt.scatter(
        anode_distance_mm,
        anode_real_raw,
        alpha=0.9,
        color="#2ca02c",
        label="Anode original S21 real",
    )
    plt.scatter(
        x_line_combined,
        y_real_combined,
        s=14,
        color="#ff7f0e",
        alpha=0.9,
        label=(
            f"Combined S21 real interp/extrap ({INTERP_STEP_MM} mm, "
            f"0..{TOTAL_LEAD_LENGTH_MM})"
        ),
    )
    plt.plot(
        x_line_combined,
        y_real_combined,
        color="#ff7f0e",
        alpha=0.9,
        linewidth=1.5,
    )
    plt.scatter(
        x_line_anode,
        y_real_anode,
        s=14,
        color="#9467bd",
        alpha=0.9,
        label=(
            f"Anode S21 real interp/extrap ({INTERP_STEP_MM} mm, "
            f"{BIFURCATION_START_MM}..{TOTAL_LEAD_LENGTH_MM})"
        ),
    )
    plt.plot(
        x_line_anode,
        y_real_anode,
        color="#9467bd",
        alpha=0.9,
        linewidth=1.5,
    )
    plt.title("Figure 1: S21 Real vs Distance to IPG")
    plt.xlabel("Distance to IPG (mm)")
    plt.ylabel("S21 Real")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    save_current_plot(
        plt,
        build_output_filename("combined_s21_real_plot__cathode_exc", "png", target_freq),
    )
    plt.show()
    plt.close()

    # Figure 2: S21 imag with original and interpolated/extrapolated data.
    plt.figure(figsize=(8, 5))
    plt.scatter(
        combined_distance_mm,
        combined_imag,
        alpha=0.9,
        color="#1f77b4",
        label="Combined original S21 imag",
    )
    plt.scatter(
        anode_distance_mm,
        anode_imag_raw,
        alpha=0.9,
        color="#2ca02c",
        label="Anode original S21 imag",
    )
    plt.scatter(
        x_line_combined,
        y_imag_combined,
        s=14,
        color="#ff7f0e",
        alpha=0.9,
        label=(
            f"Combined S21 imag interp/extrap ({INTERP_STEP_MM} mm, "
            f"0..{TOTAL_LEAD_LENGTH_MM})"
        ),
    )
    plt.plot(
        x_line_combined,
        y_imag_combined,
        color="#ff7f0e",
        alpha=0.9,
        linewidth=1.5,
    )
    plt.scatter(
        x_line_anode,
        y_imag_anode,
        s=14,
        color="#9467bd",
        alpha=0.9,
        label=(
            f"Anode S21 imag interp/extrap ({INTERP_STEP_MM} mm, "
            f"{BIFURCATION_START_MM}..{TOTAL_LEAD_LENGTH_MM})"
        ),
    )
    plt.plot(
        x_line_anode,
        y_imag_anode,
        color="#9467bd",
        alpha=0.9,
        linewidth=1.5,
    )
    plt.title("Figure 2: S21 Imag vs Distance to IPG")
    plt.xlabel("Distance to IPG (mm)")
    plt.ylabel("S21 Imag")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    save_current_plot(
        plt,
        build_output_filename("combined_s21_imag_plot__cathode_exc", "png", target_freq),
    )
    plt.show()
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.scatter(
        combined_distance_mm,
        combined_magnitude,
        alpha=0.9,
        color="#1f77b4",
        label="Original points",
    )
    plt.scatter(
        anode_distance_mm,
        anode_magnitude,
        alpha=0.9,
        color="#2ca02c",
        label="Anode original points",
    )

    # Figure 3: combined interpolation/extrapolation on 0..350 mm with 5 mm interval.
    y_line = [math.sqrt(r**2 + i**2) for r, i in zip(y_real_combined, y_imag_combined)]
    plt.scatter(
        x_line_combined,
        y_line,
        s=14,
        color="#ff7f0e",
        alpha=0.9,
        label=(
            f"Combined interp/extrap ({INTERP_STEP_MM} mm, "
            f"0..{TOTAL_LEAD_LENGTH_MM})"
        ),
    )
    plt.plot(
        x_line_combined,
        y_line,
        color="#ff7f0e",
        alpha=0.9,
        linewidth=1.5,
    )

    # Overlay anode interpolation/extrapolation on same Figure 3: 200..350 mm.
    y_anode = [math.sqrt(r**2 + i**2) for r, i in zip(y_real_anode, y_imag_anode)]
    plt.scatter(
        x_line_anode,
        y_anode,
        s=14,
        color="#9467bd",
        alpha=0.9,
        label=(
            f"Anode interp/extrap ({INTERP_STEP_MM} mm, "
            f"{BIFURCATION_START_MM}..{TOTAL_LEAD_LENGTH_MM})"
        ),
    )
    plt.plot(
        x_line_anode,
        y_anode,
        color="#9467bd",
        alpha=0.9,
        linewidth=1.5,
    )

    plt.title("Figure 3: S21 Magnitude vs Distance to IPG")
    plt.xlabel("Distance to IPG (mm)")
    plt.ylabel("S21 Magnitude")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    save_current_plot(
        plt,
        build_output_filename("combined_s21_magnitude_plot__cathode_exc", "png", target_freq),
    )
    plt.show()
    plt.close()

    # Figure 4: phase plot with the same interpolation/extrapolation settings.
    plt.figure(figsize=(8, 5))
    plt.scatter(
        combined_distance_mm,
        combined_phase,
        alpha=0.9,
        color="#1f77b4",
        label="Original points",
    )
    plt.scatter(
        anode_distance_mm,
        anode_phase,
        alpha=0.9,
        color="#2ca02c",
        label="Anode original points",
    )

    y_phase_combined = [
        math.atan2(i, r) for r, i in zip(y_real_combined, y_imag_combined)
    ]
    plt.scatter(
        x_line_combined,
        y_phase_combined,
        s=14,
        color="#ff7f0e",
        alpha=0.9,
        label=(
            f"Combined interp/extrap ({INTERP_STEP_MM} mm, "
            f"0..{TOTAL_LEAD_LENGTH_MM})"
        ),
    )
    plt.plot(
        x_line_combined,
        y_phase_combined,
        color="#ff7f0e",
        alpha=0.9,
        linewidth=1.5,
    )

    y_phase_anode = [math.atan2(i, r) for r, i in zip(y_real_anode, y_imag_anode)]
    plt.scatter(
        x_line_anode,
        y_phase_anode,
        s=14,
        color="#9467bd",
        alpha=0.9,
        label=(
            f"Anode interp/extrap ({INTERP_STEP_MM} mm, "
            f"{BIFURCATION_START_MM}..{TOTAL_LEAD_LENGTH_MM})"
        ),
    )
    plt.plot(
        x_line_anode,
        y_phase_anode,
        color="#9467bd",
        alpha=0.9,
        linewidth=1.5,
    )

    plt.title("Figure 4: S21 Phase (rad) vs Distance to IPG")
    plt.xlabel("Distance to IPG (mm)")
    plt.ylabel("S21 Phase (rad)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    save_current_plot(
        plt,
        build_output_filename("combined_s21_phase_plot__cathode_exc", "png", target_freq),
    )
    plt.show()
    plt.close()

    # Save original extracted data into:
    # ... / 03_raw_processed /
    out_csv = RAW_PROCESSED_OUTPUT_DIR / build_output_filename(
        "combined_s21_original__cathode_exc",
        "csv",
        target_freq,
    )
    save_original_csv_rows(out_csv, original_rows)

    processed_rows = []
    for d, r, i, mag, ph in zip(
        x_line_combined, y_real_combined, y_imag_combined, y_line, y_phase_combined
    ):
        processed_rows.append(
            {
                "series": "shared_to_cathode",
                "distance_to_ipg_mm": d,
                "S21_real_interp_extrap": r,
                "S21_imag_interp_extrap": i,
                "S21_magnitude_interp_extrap": mag,
                "S21_phase_rad_interp_extrap": ph,
            }
        )
    for d, r, i, mag, ph in zip(
        x_line_anode, y_real_anode, y_imag_anode, y_anode, y_phase_anode
    ):
        processed_rows.append(
            {
                "series": "anode",
                "distance_to_ipg_mm": d,
                "S21_real_interp_extrap": r,
                "S21_imag_interp_extrap": i,
                "S21_magnitude_interp_extrap": mag,
                "S21_phase_rad_interp_extrap": ph,
            }
        )

    # Save interpolated/extrapolated data into:
    # ... / 04_interpolated_extrapolated /
    processed_out_csv = INTERP_EXTRAP_OUTPUT_DIR / build_output_filename(
        "combined_s21_interp_extrap__cathode_exc",
        "csv",
        target_freq,
    )
    save_processed_csv_rows(processed_out_csv, processed_rows)


def run_branch_interp_extrap_plot(branch_dir: Path, target_freq: float):
    """Plot original and interpolated/extrapolated branch magnitude data."""
    files, s21_real_col, s21_imag_col = extract_s21_at_freq(branch_dir, target_freq)
    distance_mm = []
    magnitude = []

    print(f"\n=== {branch_dir.name} (interp/extrap for magnitude) ===")
    print("file,distance_to_ipg,S21_real,S21_imag,S21_magnitude,S21_phase_rad")
    for name, r, i in zip(files, s21_real_col, s21_imag_col):
        distance_to_ipg = extract_distance_to_ipg(name)
        d_mm = distance_token_to_mm(distance_to_ipg)
        mag = math.sqrt(r**2 + i**2)
        phase_rad = math.atan2(i, r)
        print(f"{name},{distance_to_ipg},{r},{i},{mag},{phase_rad}")
        distance_mm.append(d_mm)
        magnitude.append(mag)

    try:
        import matplotlib.pyplot as plt  # pyright: ignore[reportMissingImports]
    except ImportError:
        print("[WARN] matplotlib is not installed, skipping scatter plot.")
        return

    x_line = [
        float(x)
        for x in range(BIFURCATION_START_MM, TOTAL_LEAD_LENGTH_MM + 1, INTERP_STEP_MM)
    ]
    y_line = linear_interp_extrap(distance_mm, magnitude, x_line)

    plt.figure(figsize=(8, 5))
    plt.scatter(distance_mm, magnitude, alpha=0.9, label="Original points")
    plt.scatter(
        x_line,
        y_line,
        s=14,
        color="orange",
        alpha=0.9,
        label="Linear interp/extrap points (5 mm)",
    )
    plt.title(f"{branch_dir.name} S21 Magnitude vs Distance to IPG")
    plt.xlabel("Distance to IPG (mm)")
    plt.ylabel("S21 Magnitude")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.close()


if __name__ == "__main__":
    create_run_folder_tree()
    prompt_user_to_place_raw_files()
    validate_required_raw_data()

    run_branch_analysis(ANODE_RAW_DIR, TARGET_FREQ)
    run_branch_analysis(CATHODE_RAW_DIR, TARGET_FREQ)
    run_branch_analysis(SHARED_RAW_DIR, TARGET_FREQ)
    run_combined_shared_then_cathode(TARGET_FREQ)

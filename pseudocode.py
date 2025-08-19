import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import re

# Configure matplotlib for professional appearance with math support
plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["DejaVu Serif", "Computer Modern Roman", "Times New Roman"],
        "font.size": 11,
        "mathtext.fontset": "cm",  # Computer Modern math font
    }
)


def render_text_with_bold(ax, x, y, text, fontsize=11, fontweight="normal", **kwargs):
    """Render text with **bold** formatting properly handled"""
    # Split text by **bold** markers
    parts = re.split(r"\*\*(.*?)\*\*", text)

    current_x = x
    for i, part in enumerate(parts):
        if not part:  # Skip empty parts
            continue

        # Odd indices are bold (inside **)
        weight = "bold" if i % 2 == 1 else fontweight

        # Render this part
        text_obj = ax.text(
            current_x, y, part, fontsize=fontsize, fontweight=weight, transform=ax.transAxes, **kwargs
        )

        # Get the rendered width to position next part
        renderer = ax.figure.canvas.get_renderer()
        bbox = text_obj.get_window_extent(renderer)
        # Convert back to axes coordinates
        bbox_axes = bbox.transformed(ax.transAxes.inverted())
        current_x = bbox_axes.x1


# Algorithm content - Automated Restraint Selection with RestraintSetter
algorithm_lines = [
    ("title", "Algorithm 1: Automated Restraint Selection with RestraintSetter"),
    (
        "require",
        r"Input: molA, molB (3D molecular structures), atom_compare_method, strict_surround, ignore_surround_atom_type",
    ),
    ("ensure", r"Output: restraints (dictionary mapping atoms from molA to molB for positional restraints)"),
    ("step", r"**Initialize RestraintSetter:**"),
    ("substep", r"Load molA and molB"),
    ("substep", r"Generate initial atom mapping using Kartograf"),
    ("step", r"**Process Rings Separately** (process_rings_separately):"),
    ("substep", r"Identify all ring structures in molA and molB"),
    ("substep", r"Map rings between molecules based on initial Kartograf mapping"),
    ("substep", r"**for each** mapped ring pair **do**"),
    ("subsubstep", r"Identify atoms within rings and their substituents"),
    ("subsubstep", r"Detect and categorize ring-to-ring connections"),
    ("step", r"**Compare Molecule Rings** (compare_molecule_rings):"),
    ("substep", r"**for each** pair of processed rings **do**"),
    ("subsubstep", r"Assess ring equivalence based on atom_compare_method"),
    ("subsubstep", r"**if** strict_surround **then** compare ring substituents"),
    ("subsubstep", r"**if** ignore_surround_atom_type **then** use less strict substituent comparison"),
    ("subsubstep", r"**if** rings (and optionally substituents) are equivalent **then**"),
    ("subsubsubstep", r"Mark corresponding atoms for restraint"),
    ("subsubstep", r"**else**"),
    ("subsubsubstep", r"Exclude atoms from restraints unless part of crucial ring-to-ring linkage"),
    ("step", r"**Set Restraints** (set_restraints):"),
    ("substep", r"**return** dictionary with all atoms marked for restraint"),
]

# Create figure with dimensions to accommodate the algorith
fig, ax = plt.subplots(figsize=(14.2, 8))
ax.axis("off")

# Add top and bottom lines (LaTeX algorithmic style) instead of full border
top_line = mpatches.Rectangle((0.02, 0.85), 0.96, 0.002, linewidth=0, facecolor="black", alpha=0.8)
title_bottom_line = mpatches.Rectangle((0.02, 0.770), 0.96, 0.002, linewidth=0, facecolor="black", alpha=0.8)
bottom_line = mpatches.Rectangle((0.02, 0), 0.96, 0.002, linewidth=0, facecolor="black", alpha=0.8)
ax.add_patch(top_line)
ax.add_patch(title_bottom_line)
ax.add_patch(bottom_line)

# Render the algorithm with LaTeX-style spacing
y_pos = 0.82  # Start below the top line
line_spacing = 0.032  # Much tighter spacing like LaTeX

# Initialize line counter for algorithmic numbering
line_number = 1

for line_type, content in algorithm_lines:
    if line_type == "title":
        ax.text(
            0.5, y_pos, content, fontsize=14, fontweight="bold", ha="center", va="top", transform=ax.transAxes
        )
        y_pos -= line_spacing * 2.5  # Space after title
    elif line_type == "require":
        render_text_with_bold(ax, 0.08, y_pos, content, fontsize=11, fontweight="bold", ha="left", va="top")
        y_pos -= line_spacing * 1.2
    elif line_type == "ensure":
        render_text_with_bold(ax, 0.08, y_pos, content, fontsize=11, fontweight="bold", ha="left", va="top")
        y_pos -= line_spacing * 1.5  # Space before algorithm steps
    elif line_type in ["step", "substep", "subsubstep", "subsubsubstep"]:
        # Add line number for algorithmic steps
        ax.text(
            0.06,
            y_pos,
            f"{line_number}:",
            fontsize=11,
            fontweight="normal",
            ha="right",
            va="top",
            transform=ax.transAxes,
        )

        # Determine indentation based on step type
        if line_type == "step":
            x_indent = 0.08
        elif line_type == "substep":
            x_indent = 0.12
        elif line_type == "subsubstep":
            x_indent = 0.16
        elif line_type == "subsubsubstep":
            x_indent = 0.20

        render_text_with_bold(ax, x_indent, y_pos, content, fontsize=11, ha="left", va="top")
        y_pos -= line_spacing
        line_number += 1

# Save in multiple high-quality formats for different journal requirements
plt.savefig("algorithm_figure.png", bbox_inches="tight", dpi=300, pad_inches=0.2)
plt.savefig("algorithm_figure.svg", bbox_inches="tight", pad_inches=0.2)

print("Algorithm figures generated!")
print("Files: algorithm_figure.png, algorithm_figure.svg")

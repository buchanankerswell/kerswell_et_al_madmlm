import os
import glob
from rocml import (
    parse_arguments,
    check_arguments,
    print_filepaths,
    train_rocml,
    combine_plots_vertically,
    combine_plots_horizontally
)

# Parse arguments and check
args = parse_arguments()
valid_args = check_arguments(args, "train-benchmark-rocmls.py")

# Load valid arguments
locals().update(valid_args)

# Test for results
mgm_results_train = len(os.listdir(f"{outdir}/{sampleid}/magemin_train_{res}")) != 0
mgm_results_valid = len(os.listdir(f"{outdir}/{sampleid}/magemin_valid_{res}")) != 0
ppx_results_train = len(os.listdir(f"{outdir}/{sampleid}/perplex_train_{res}")) != 0
ppx_results_valid = len(os.listdir(f"{outdir}/{sampleid}/perplex_valid_{res}")) != 0

if (mgm_results_train and ppx_results_train and mgm_results_valid and ppx_results_valid):
    for m in models:
        # Run support vector regression
        train_rocml(
            sampleid, res, params, True, True, True, m, tune, kfolds,
            parallel, nprocs, seed, colormap, outdir, figdir, datadir
        )

        # Change model string for filename
        mlab = m.replace(" ", "-")

        for p in params:
            if p in ["DensityOfFullAssemblage", "Vp", "Vs"]:
                # First row
                combine_plots_horizontally(
                    f"{figdir}/MAGEMin-{sampleid}-{p}-{mlab}-prem.png",
                    f"{figdir}/Perple_X-{sampleid}-{p}-{mlab}-prem.png",
                    f"{figdir}/prem-{sampleid}-{p}-{mlab}.png",
                    caption1="a)",
                    caption2="b)"
                )

            # First row
            combine_plots_horizontally(
                f"{figdir}/MAGEMin-{sampleid}-{p}-{mlab}-targets-surf.png",
                f"{figdir}/Perple_X-{sampleid}-{p}-{mlab}-targets-surf.png",
                f"{figdir}/temp1.png",
                caption1="a)",
                caption2="b)"
            )

            # Second row
            combine_plots_horizontally(
                f"{figdir}/MAGEMin-{sampleid}-{p}-{mlab}-surf.png",
                f"{figdir}/Perple_X-{sampleid}-{p}-{mlab}-surf.png",
                f"{figdir}/temp2.png",
                caption1="c)",
                caption2="d)"
            )

            # Third row
            combine_plots_horizontally(
                f"{figdir}/MAGEMin-{sampleid}-{p}-{mlab}-diff-surf.png",
                f"{figdir}/Perple_X-{sampleid}-{p}-{mlab}-diff-surf.png",
                f"{figdir}/temp4.png",
                caption1="e)",
                caption2="f)"
            )

            # Stack rows
            combine_plots_vertically(
                f"{figdir}/temp1.png",
                f"{figdir}/temp2.png",
                f"{figdir}/temp3.png",
                caption1="",
                caption2=""
            )

            # Stack rows
            combine_plots_vertically(
                f"{figdir}/temp3.png",
                f"{figdir}/temp4.png",
                f"{figdir}/surf-{sampleid}-{p}-{mlab}.png",
                caption1="",
                caption2=""
            )

            # First row
            combine_plots_horizontally(
                f"{figdir}/MAGEMin-{sampleid}-{p}-{mlab}-targets.png",
                f"{figdir}/Perple_X-{sampleid}-{p}-{mlab}-targets.png",
                f"{figdir}/temp1.png",
                caption1="a)",
                caption2="b)"
            )

            # Second row
            combine_plots_horizontally(
                f"{figdir}/MAGEMin-{sampleid}-{p}-{mlab}-predictions.png",
                f"{figdir}/Perple_X-{sampleid}-{p}-{mlab}-predictions.png",
                f"{figdir}/temp2.png",
                caption1="c)",
                caption2="d)"
            )

            # Third row
            combine_plots_horizontally(
                f"{figdir}/MAGEMin-{sampleid}-{p}-{mlab}-diff.png",
                f"{figdir}/Perple_X-{sampleid}-{p}-{mlab}-diff.png",
                f"{figdir}/temp4.png",
                caption1="e)",
                caption2="f)"
            )

            # Stack rows
            combine_plots_vertically(
                f"{figdir}/temp1.png",
                f"{figdir}/temp2.png",
                f"{figdir}/temp3.png",
                caption1="",
                caption2=""
            )

            # Stack rows
            combine_plots_vertically(
                f"{figdir}/temp3.png",
                f"{figdir}/temp4.png",
                f"{figdir}/image-{sampleid}-{p}-{mlab}.png",
                caption1="",
                caption2=""
            )

    os.remove(f"{figdir}/temp1.png")
    os.remove(f"{figdir}/temp2.png")
    os.remove(f"{figdir}/temp3.png")
    os.remove(f"{figdir}/temp4.png")

    # Model labels
    mlabs = [m.replace(" ", "-") for m in models]

    if len(mlabs) == 8:

        # First row
        combine_plots_horizontally(
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[0]}-targets-surf.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[0]}-surf.png",
            f"{figdir}/temp1.png",
            caption1="a)",
            caption2="b)"
        )

        # Second row
        combine_plots_horizontally(
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[1]}-surf.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[2]}-surf.png",
            f"{figdir}/temp2.png",
            caption1="e)",
            caption2="f)"
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/temp1.png",
            f"{figdir}/temp2.png",
            f"{figdir}/temp3.png",
            caption1="",
            caption2=""
        )

        # Third row
        combine_plots_horizontally(
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[3]}-surf.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[7]}-surf.png",
            f"{figdir}/temp4.png",
            caption1="c)",
            caption2="d)"
        )

        # Fourth row
        combine_plots_horizontally(
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[4]}-surf.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[6]}-surf.png",
            f"{figdir}/temp5.png",
            caption1="g)",
            caption2="h)"
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/temp4.png",
            f"{figdir}/temp5.png",
            f"{figdir}/temp6.png",
            caption1="",
            caption2=""
        )

        # Stack columns
        combine_plots_horizontally(
            f"{figdir}/temp3.png",
            f"{figdir}/temp6.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-model-comp-surf.png",
            caption1="",
            caption2=""
        )

        # First row
        combine_plots_horizontally(
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[0]}-targets-surf.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[0]}-surf.png",
            f"{figdir}/temp1.png",
            caption1="i)",
            caption2="j)"
        )

        # Second row
        combine_plots_horizontally(
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[1]}-surf.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[2]}-surf.png",
            f"{figdir}/temp2.png",
            caption1="m)",
            caption2="n)"
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/temp1.png",
            f"{figdir}/temp2.png",
            f"{figdir}/temp3.png",
            caption1="",
            caption2=""
        )

        # Third row
        combine_plots_horizontally(
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[3]}-surf.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[7]}-surf.png",
            f"{figdir}/temp4.png",
            caption1="k)",
            caption2="l)"
        )

        # Fourth row
        combine_plots_horizontally(
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[5]}-surf.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[6]}-surf.png",
            f"{figdir}/temp5.png",
            caption1="o)",
            caption2="p)"
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/temp4.png",
            f"{figdir}/temp5.png",
            f"{figdir}/temp6.png",
            caption1="",
            caption2=""
        )

        # Stack columns
        combine_plots_horizontally(
            f"{figdir}/temp3.png",
            f"{figdir}/temp6.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-model-comp-surf.png",
            caption1="",
            caption2=""
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/MAGEMin-{sampleid}-{p}-model-comp-surf.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-model-comp-surf.png",
            f"{figdir}/all-surf-{sampleid}-{p}.png",
            caption1="",
            caption2=""
        )

        # First row
        combine_plots_horizontally(
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[0]}-targets.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[0]}-predictions.png",
            f"{figdir}/temp1.png",
            caption1="a)",
            caption2="b)"
        )

        # Second row
        combine_plots_horizontally(
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[1]}-predictions.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[2]}-predictions.png",
            f"{figdir}/temp2.png",
            caption1="e)",
            caption2="f)"
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/temp1.png",
            f"{figdir}/temp2.png",
            f"{figdir}/temp3.png",
            caption1="",
            caption2=""
        )

        # Third row
        combine_plots_horizontally(
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[3]}-predictions.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[7]}-predictions.png",
            f"{figdir}/temp4.png",
            caption1="c)",
            caption2="d)"
        )

        # Fourth row
        combine_plots_horizontally(
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[4]}-predictions.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[6]}-predictions.png",
            f"{figdir}/temp5.png",
            caption1="g)",
            caption2="h)"
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/temp4.png",
            f"{figdir}/temp5.png",
            f"{figdir}/temp6.png",
            caption1="",
            caption2=""
        )

        # Stack columns
        combine_plots_horizontally(
            f"{figdir}/temp3.png",
            f"{figdir}/temp6.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-model-comp-image.png",
            caption1="",
            caption2=""
        )

        # First row
        combine_plots_horizontally(
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[0]}-targets.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[0]}-predictions.png",
            f"{figdir}/temp1.png",
            caption1="i)",
            caption2="j)"
        )

        # Second row
        combine_plots_horizontally(
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[1]}-predictions.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[2]}-predictions.png",
            f"{figdir}/temp2.png",
            caption1="m)",
            caption2="n)"
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/temp1.png",
            f"{figdir}/temp2.png",
            f"{figdir}/temp3.png",
            caption1="",
            caption2=""
        )

        # Third row
        combine_plots_horizontally(
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[3]}-predictions.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[7]}-predictions.png",
            f"{figdir}/temp4.png",
            caption1="k)",
            caption2="l)"
        )

        # Fourth row
        combine_plots_horizontally(
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[5]}-predictions.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[6]}-predictions.png",
            f"{figdir}/temp5.png",
            caption1="o)",
            caption2="p)"
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/temp4.png",
            f"{figdir}/temp5.png",
            f"{figdir}/temp6.png",
            caption1="",
            caption2=""
        )

        # Stack columns
        combine_plots_horizontally(
            f"{figdir}/temp3.png",
            f"{figdir}/temp6.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-model-comp-image.png",
            caption1="",
            caption2=""
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/MAGEMin-{sampleid}-{p}-model-comp-image.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-model-comp-image.png",
            f"{figdir}/all-image-{sampleid}-{p}.png",
            caption1="",
            caption2=""
        )

        # First row
        combine_plots_horizontally(
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[0]}-prem.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[1]}-prem.png",
            f"{figdir}/temp1.png",
            caption1="a)",
            caption2="b)"
        )

        # Second row
        combine_plots_horizontally(
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[2]}-prem.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[3]}-prem.png",
            f"{figdir}/temp2.png",
            caption1="e)",
            caption2="f)"
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/temp1.png",
            f"{figdir}/temp2.png",
            f"{figdir}/temp3.png",
            caption1="",
            caption2=""
        )

        # Third row
        combine_plots_horizontally(
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[4]}-prem.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[5]}-prem.png",
            f"{figdir}/temp4.png",
            caption1="c)",
            caption2="d)"
        )

        # Fourth row
        combine_plots_horizontally(
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[6]}-prem.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-{mlabs[7]}-prem.png",
            f"{figdir}/temp5.png",
            caption1="g)",
            caption2="h)"
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/temp4.png",
            f"{figdir}/temp5.png",
            f"{figdir}/temp6.png",
            caption1="",
            caption2=""
        )

        # Stack columns
        combine_plots_horizontally(
            f"{figdir}/temp3.png",
            f"{figdir}/temp6.png",
            f"{figdir}/MAGEMin-{sampleid}-{p}-model-comp-prem.png",
            caption1="",
            caption2=""
        )

        # First row
        combine_plots_horizontally(
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[0]}-prem.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[1]}-prem.png",
            f"{figdir}/temp1.png",
            caption1="i)",
            caption2="j)"
        )

        # Second row
        combine_plots_horizontally(
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[2]}-prem.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[3]}-prem.png",
            f"{figdir}/temp2.png",
            caption1="m)",
            caption2="n)"
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/temp1.png",
            f"{figdir}/temp2.png",
            f"{figdir}/temp3.png",
            caption1="",
            caption2=""
        )

        # Third row
        combine_plots_horizontally(
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[4]}-prem.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[5]}-prem.png",
            f"{figdir}/temp4.png",
            caption1="k)",
            caption2="l)"
        )

        # Fourth row
        combine_plots_horizontally(
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[6]}-prem.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-{mlabs[7]}-prem.png",
            f"{figdir}/temp5.png",
            caption1="o)",
            caption2="p)"
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/temp4.png",
            f"{figdir}/temp5.png",
            f"{figdir}/temp6.png",
            caption1="",
            caption2=""
        )

        # Stack columns
        combine_plots_horizontally(
            f"{figdir}/temp3.png",
            f"{figdir}/temp6.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-model-comp-prem.png",
            caption1="",
            caption2=""
        )

        # Stack rows
        combine_plots_vertically(
            f"{figdir}/MAGEMin-{sampleid}-{p}-model-comp-prem.png",
            f"{figdir}/Perple_X-{sampleid}-{p}-model-comp-prem.png",
            f"{figdir}/all-prem-{sampleid}-{p}.png",
            caption1="",
            caption2=""
        )

    # Clean up directory
    tmp_files = glob.glob(f"{figdir}/temp*.png")
    mgm_files = glob.glob(f"{figdir}/MAGEMin*.png")
    ppx_files = glob.glob(f"{figdir}/Perple_X*.png")

    for file in tmp_files + mgm_files + ppx_files:
        os.remove(file)

# Print figure filepaths
print_filepaths(figdir)
print("train-benchmark-rocmls.py done!")
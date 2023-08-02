# Introduction

The dominant mineral phases in Earth's upper mantle are olivine, ringwoodite, bridgmanite, and ferropericlase [@ringwood1975; @ringwood1991], comprising up to 60–90% of the mantle's volume [e.g., @stixrude2012]. These Mg-Fe-rich phases form by a series of discrete reactions (@eq:mantle-transitions) that define mantle transition zones (MTZs) near 410 km and 660 km depths beneath Earth's surface. MTZs are characterized by relatively sharp boundaries with contrasting physical properties [e.g, density and elasticity, @dziewonski1981; @ita1992] that strongly impact mantle convection, melting, and plate tectonics [@fukao2001; @ringwood1991; @schubert1975; @kuritani2019; @karato2001; @wang2015; @jenkins2016].

\begin{align}
	\text{olivine} \xrightarrow{\text{410 km}} \text{ringwoodite} &\xrightarrow{\text{660 km}} \text{bridgmanite} + \text{ferropericlase} \label{eq:mantle-transitions} \\
	\text{(Mg,Fe)}_{2}\text{SiO}_{4} \xrightarrow{\text{410 km}} \text{(Mg,Fe)}_{2}\text{SiO}_{4} &\xrightarrow{\text{660 km}} \text{(Mg,Fe)}\text{SiO}_{3} + \text{(Mg,Fe)}\text{O} \nonumber
\end{align}

Although the physio-chemical nature of MTZs remains under vigorous investigation [@goes2022; @pearson2014; @yoshino2008; @waszek2021; @kiseeva2018; @fei2017; @zhou2022], modelling the interplay between plate tectonics and MTZs is possible with numerical geodynamic simulations of mantle flow that implement pressure-temperature (PT)-dependent phase changes (e.g., @eq:mantle-transitions). This approach has generated many important hypotheses implicating MTZs as critical features controlling global plate tectonics and water cycling in the deep Earth [e.g., @agrusta2017; @li2019; @torii2007; @yang2020]. However, the tendency to assume fixed mantle compositions that neglect chemical fractionation from fluid-rock interactions and partial melting limit such numerical experiments to rough first-order approximations of true mantle flow.

Advancing towards more comprehensive models of plate interactions at MTZs requires a leap from modelling PT- to PT-composition-time (PTXt)-dependent phase changes in the mantle. This is currently intractable, however, because Gibbs Free Energy Minimization (GFEMs) programs [e.g., @connolly2009; @riel2022] used to calculate PTX-dependent phase relations---referred to as mineral assemblage diagrams, or MADs---remain slow (10$^2$–10$^4$ seconds; [@fig:benchmark-times]). While recent parallelized GFEM programs [@riel2022] have increased efficiency dramatically ([@tbl:benchmark-times-table]), computing MADs iteratively during geodynamic simulations requires GFEM efficiency on the order of $\leq$ 10 milliseconds to be feasible. A rate of improvement from 10$^2$ to 10$^{-2}$ seconds seems unlikely within the current GFEM paradigm, however, and applying parallelization across thousands of CPU/GPU cores is inaccessible in many cases.

![Computational efficieincy for GFEM programs MAGEMin (dashed lines with squares) and Perple_X (solid lines with circles). Note that MAGEMin was ran in parallel on 6 CPU cores, while Perple_X has no parallel capabilities. In the best case for a 128x128 resolution PT grid, stable phase relations (i.e., MADs) take 171.2 seconds to compute (@tbl:benchmark-times-table).](assets/figs/benchmark-times.png){#fig:benchmark-times}

Here we propose an alternative approach for inferring MADs using pre-trained machine learning models (referred to as MADMLMs). We hypothesize that MADMLMs can improve efficiency by up to 4 orders of magnitude versus incumbent GFEM programs for computing PTXt-dependent phase changes in the mantle. If true, real-time inference of PTXt-dependent phase changes at the individual node-scale in geodynamic simulations will be feasible---enabling new models of global tectonic plate behavior, deep water cycling, and mantle melting at MTZs. If false, we will demonstrate the practical limitations of applying neural networks to petrological datasets---a critical step for discovering alternative approaches for implementing PTXt-dependent phase changes in numerical geodynamic simulations.

# Methods {#sec:methods}

The following sections describe our design decisions for building training datasets (i.e., MADs) and validating various MADMLMs. Our objectives are threefold. First, design the size (PT range) and scope (chemical compositions) of MADMLM training data to ensure widespread applicability of MADMLMs to geodynamic problems within the upper mantle (@sec:design-training-data). Second, compute minimal MADMLM training data as described in @sec:design-training-data and compare the efficiencies of MAGEMin and Perple_X (@sec:build-training-data). Third, train various MADMLMs and determine the best models by k-fold cross-validation (@sec:training-MADMLMs). Comparisons among MAGEMin, Perple_X, and MADMLMs are then detailed in @sec:results.

## Designing MADMLM Training Datasets {#sec:design-training-data}

### PT Conditions

High-pressure experiments constrain the reaction $\text{olivine} \xrightarrow{\text{410 km}} \text{ringwoodite}$ between 14.0 ± 1.0 GPa and 1600 ± 400 K with Clapeyron slopes between 2.4x10$^{-3}$ ± 1.4x10$^{-3}$ GPa/K  [@akaogi1989; @katsura1989; @morishima1994; @li2019]. Likewise, the reaction $\text{ringwoodite} \xrightarrow{\text{660 km}} \text{bridgmanite} + \text{ferropericlase}$ is constrained between 24.0 ± 1.5 GPa and 1600 ± 400 K with negative Clapeyron slopes between -2.0x10$^{-3}$ ± 1.6x10$^{-3}$ GPa/K  [@akaogi2007; @bina1994; @litasov2005; @katsura2003; @ito1990; @ito1982; @ito1989a; @ito1989b; @hirose2002; @ishii2018]. We therefore compute MADMLM training data within a rectangular PT region bound between 1.0–28.0 GPa and 773–2273 K to encompass expected conditions for the entire upper mantle---from the base of the Moho at 35 km to the 660 km MTZ ([@fig:training-pt-range]).

![PT diagram showing experimentally-derived phase boundaries for the 410 and 660 km MTZs (colored lines), the range of PT conditions for computing MADLML training data (shaded grey box), and the range of expected mantle conditions (shaded blue box with hatches). Geotherm 1 (solid black line) assumes a mantle potential temperature of 273 K with a 1 K/km thermal gradient. Geotherm 2 (dashed black line) assumes a mantle potential temperature of 1773 K with a  0.5 K/km thermal gradient. Phase boundaries are calculated after @li2019.](assets/figs/training-pt-range.png){#fig:training-pt-range}

@fig:training-pt-range shows that our training dataset design includes conditions that are not expected to exist in the upper mantle, nor typically modelled during geodynamic simulations [e.g., very cold conditions at thermal gradients $\leq$ 5 K/km, @maruyama1996; @syracuse2010]. Thus, training MADMLMs on the entire dataset can be considered impractical with respect to efficiency (unnecessarily large training set size) and accuracy (some PT conditions lie outside of the bounds of calibrated thermodynamic data). For example, MAD results can be spurious and noisy at very low-temperature and high-pressure (e.g., at 20 GPa and 1000 K) and include high degrees of partial melt not expected to exist in the mantle at very low-pressure and high-temperature (e.g., at 5 GPa and 2000 K).

On the other hand, a regular rectangular training dataset design is more straightforward to compute,  validate, and benchmark. Moreover, size inefficiencies and inaccuracies at extreme PT conditions will only affect MADMLMs at training time, not during inference (i.e., prediction). For example, unknown PTs input into MADMLMs for inference (e.g., from a geodynamic simulation) should be within the PT range where MADMLM training data are most accurate (blue hatched region in @fig:training-pt-range). Thus, MADMLM predictions should be no less accurate than MAGEMin or Perple_X---assuming MADMLMs fit the training data well. Performance metrics for MADMLM fitting are detailed in @sec:comparing-MADMLMs.

### Solution Phase Models and Thermodynamic Data {#sec:thermodynamic-data}

Thermodynamic data for computing MADMLM training datasets are based on end-member thermodynamic properties from @holland2018, with updates from @tomlinson2021 and @holland2022. The database (tc-ds634.txt from [hpxeosandthermocalc.org](https://hpxeosandthermocalc.org)) is specifically formulated for calculating phase relations for a wide array of igneous rocks and melt compositions. @holland2018 itself is an extension of the foundational database from @holland2011, which is calibrated up to 300 GPa and 2000 ˚C. Thus, the dataset tc-ds634.txt is appropriate for building MADMLM training datasets for the entire upper mantle ([@fig:training-pt-range]).

All GFEM calculations are computed with equations of state for pure phases: quartz, coesite, stishovite, kyanite, corundum, and rutile, and solution phases: feldspar, spinel, garnet, clinopyroxene, orthopyroxene, olivine, ilmenite, and silicate melt. The same solution models from @holland2018 are used for MAGEMin and Perple_X calculations. The one notable exception is ternary feldspar models, which differ for MAGEMin [after @holland2022] and Perple_X [after @fuhrman1988].

More importantly, Perple_X includes solution models for wadsleyite, ringwoodite, wuestite, perovskite, ferropericlase, and high-pressure clinopyroxene that are not included in the current release of MAGEMin (version 1.3.2, June 6, 2023). To make Perple_X calculations approximately identical to MAGEMin, the pure end-member phases for wadsleyite, ringwoodite, wuestite, perovskite, ferropericlase, and high-pressure clinopyroxene are used without solution models. This issue will be addressed in future releases of MAGEMin software, which will include solution models for deep mantle phases (Riel, [personal communications](https://github.com/ComputationalThermodynamics/MAGEMin/issues/61), July 11, 2023).

### Bulk Chemical Compositions

Existing estimates for the bulk chemical composition of the upper mantle are based on analyses of high-pressure-high-temperature melting experiments and mantle-derived xenoliths, kimberlites, and basalts [e.g., @allegre1984; @green1979; @ringwood1962; @jagoutz1979; @sun1982; @ringwood1991; @palme2003; @stracke2021]. [@tbl:benchmark-comps] provides some well-referenced examples, including hypothetical mantle compositions with varying degrees of differentiation by partial melting [Primitive Upper Mantle: PUM, and Depleted MORB Mantle: DMM, @sun1989; @workman2005], as well as real and hypothetical products of mantle melting [Iclandic Basalt: RE46, and Normal MORB: NMORB, @gale2013; @yang1996]. MADMLM training data are currently fixed at PUM, which represents the average bulk (pyrolitic) composition of the upper mantle. Eventually, training data will include all compositions in @tbl:benchmark-comps to approximate a more complete range of expected compositions for the upper mantle.

{{ benchmark-comps.md }}
: Estimated bulk chemical compositions (in wt. % oxides) for the upper mantle. {#tbl:benchmark-comps}

## Computing MADMLM Training Datasets {#sec:build-training-data}

We use the GFEM programs [MAGEMin](https://github.com/ComputationalThermodynamics/MAGEMin) and [Perple_X](https://github.com/ondrolexa/Perple_X) [@riel2022; @connolly2009] to compute MADMLM training data for a broad range of upper mantle PT conditions. The two programs use slightly different computational approaches to minimize the total GFE of a multicomponent multiphase thermodynamic system. At a fixed PT, the GFE for such a system is defined by the following equation [@gibbs1878; @spear1993]:

\begin{equation}
	\text{GFE} = \sum_{\lambda=1}^{\Lambda} p_{\lambda} \sum_{n=1}^{N} p_n \mu_n + \sum_{\omega=1}^{\Omega} p_{\omega} \mu_{\omega} \label{eq:gfe}
\end{equation}

\noindent where $\Lambda$ is the number solution phases, $N$ is the number of end-member compounds that mix to form solution phases, and $\Omega$ is the number of pure (stoichiometric) phases. Thus, @eq:gfe states that the total GFE of a thermodynamic system (at a fixed PT) is the weighted sum of the molar fractions $p_{\lambda}$ of solution phases $\lambda$ and the molar fractions $p_n$ and chemical potentials $\mu_n$ of end-member compounds $n$ that mix to form solution phases $\lambda$, plus the weighted sum of the molar fractions $p_{\omega}$ and chemical potentials $\mu_{\omega}$ of pure phases $\omega$.

For pure phases, the chemical potential is a constant [@spear1993]:

\begin{equation}
	\mu_{\omega} = \text{GFE}_{\omega}^{\text{standard}}
\end{equation}

\noindent where $\text{GFE}_{\omega}^{\text{standard}}$ is the Gibbs Free Energy of formation at standard PT (1 bar, 273 K). For a solution phase, however, the chemical potential is described by a non-ideal mixture of end-member compounds:

\begin{equation}
	\mu_n = \text{GFE}_n^{\text{standard}} + RTln(a_n^{\text{ideal}}) + \text{GFE}_n^{\text{excess}}
\end{equation}

\noindent where $\mu_n$ is the chemical potential of end-member compound $n$, $R$ is the gas constant, $T$ is temperature, $a_n^{\text{ideal}}$ is the activity of an end-member compound defined by ideal mixing: $a_n^{\text{ideal}} = x_n$, where $x_n$ is the molar fraction of the end-member compound $n$. The $\text{GFE}_n^{\text{excess}}$ term models non-ideal behavior by defining symmetric (site-independent) and asymmetric (site-dependent) mixing of end-member compounds on different crystallographic sites for a particular solution phase $\lambda$ [mixing-on-site formalism, @holland2003; @powell1993].

Additional compositional constraints are imposed on @eq:gfe by the Gibbs-Duhem equation [@spear1993]:

\begin{equation}
	\mu_{(\omega,n)} = \sum_{c=1}^{C} \mu_c a_{(\omega,n) c} \label{eq:gibbs-duhem}
\end{equation}

\noindent where $C$ is the number of chemical components (oxides) considered in the thermodynamic system. The Gibbs-Duhem equation states that the total chemical potential of a pure or solution phase $\mu_{(\omega,n)}$ is equal to the weighted sum of the chemical potentials of each oxide $\mu_c$ and the activities of each oxide in each end-member compound $a_{(\omega,n) c}$.

@eq:gibbs-duhem implies that the total GFE of the thermodynamic system is dependent on its bulk chemical composition. Consequently, for a fixed bulk composition at equilibrium, the stable mineral assemblage must satisfy the Gibbs phase rule:

\begin{equation}
	F = C - \Phi + 2
\end{equation}

\noindent where $F$ is the number of degrees of freedom, $C$ is the number of chemical components (oxides), and $\Phi$ is the number of stable mineral phases in the rock. In this case, the "degrees of freedom" $F$ refers to the number of independent mineral phases that can vary their chemical potentials while the system remains in equilibrium.

Lastly, conservation of mass is maintained by equating the sum total of the chemical potentials in the system to the bulk rock composition:

\begin{equation}
	\sum_{c=1}^{C} \sum_{\lambda=1}^{\Lambda} p_{\lambda} \sum_{n=1}^{N} a_{nc} p_n + \sum_{c=1}^{C} \sum_{\omega=1}^{\Omega} p_{\omega} a_{\omega c} = \sum_{c=1}^{C} \text{bulk-rock}_c \label{eq:mass-balance}
\end{equation}

In principle, applying identical sets of solution phase models, thermodynamic data, and bulk compositions to the above equations will define identical GFE hyperplanes (i.e. define the same G-X "surfaces" in multidimensional space). This implies that GFEM programs should converge on identical MADs irrespective of the minimization algorithm. We can therefore expect similar results between MAGEMin and Perple_X when comparing the two programs with the same bulk compositions and thermodynamic data. Benchmarking results for MAGEMin and Perple_X are detailed in @sec:comparing-GFEs.

## Training MADMLMs {#sec:training-MADMLMs}

MADs produced by MAGEMin and Perple_X were preprocessed before training using the following procedure. First, the square 2D MADs $Z = (z_{1,1}, z_{1,2}, \ldots, z_{1,W}, z_{2,1}, z_{2,2}, \ldots, z_{2,W}, z_{3,1}, z_{3,2}, \ldots, z_{W,W})$ are separated into a flat 2D feature array of PTs $X = (x_{1,1}, x_{1,2}, x_{2,1}, x_{2,2}, \ldots, x_{V,1}, x_{V,2})$ and 1D target array of a single rock property $y = (y_1, y_2, \ldots, y_V)$, where $V = W^2$ is the total number of training data points (i.e. the MAD grid size). Next, the feature array $X$ and target array $y$ are standardized by shifting their values by their means and dividing by their standard deviations, respectively:

\begin{align}
	X_{V,1}^{\text{standardized}} &= \frac{X_{V,1} - \mu_{X_{V,1}}}{\sigma_{X_{V,1}}} \label{eq:standard-scaler} \\
	X_{V,2}^{\text{standardized}} &= \frac{X_{V,2} - \mu_{X_{V,2}}}{\sigma_{X_{V,2}}} \nonumber \\
	y_{V}^{\text{standardized}} &= \frac{y_{V} - \mu_{y_{V}}}{\sigma_{y_{V}}} \nonumber
\end{align}

\noindent where $X_{V,1}^{\text{standardized}}$ are the standardized Ps, $X_{V,2}^{\text{standardized}}$ are the standardized Ts, $y_{V}^{\text{standardized}}$ are the standardized rock property (density in this case), $\mu$ is the mean and $\sigma$ is the standard deviation of the appropriate array. This so-called "z-score normalization" is a necessary step before MADMLM training because the difference in magnitude of the feature values (1-28 GPa vs. 773-2273 K) results in poor performance for MADMLMs that use distance-metrics for fitting.

The preprocessed training data were then fit with eight different non-linear ML models (@tbl:madmlm-descriptions). Each model used standard parameters from the scikit-learn python library [@scikit2011] except for K Nearest, which was fit using a distance-weighting scheme instead of uniform weighting of the k-nearest data points. For Neural Networks, dense (fully-connected) layers were used with constant layer sizes equal to the total number of training data $V$ divided by 100 and rounded down to the nearest integer. The reader is referred to the scikit-learn [documentation](https://scikit-learn.org/stable/supervised_learning.html#supervised-learning) on regression models for more specifics.

{{ madmlms.md }}
: Advantages and disadvantages of various non-linear ML models. {#tbl:madmlm-descriptions}

Finally, average performance metrics for each model were evaluated using a k-fold cross-validation technique as follows. First, the training data are partitioned into k = 30 non-overlapping folds of $V$/k samples, where $V$ is the total number of training data points (i.e., the MAD grid size). To reduce the impact of inherent ordering in the data, the data are shuffled before splitting into folds. Cross-validation then proceeds with k iterations, where in each iteration, models are trained on samples from k-1 folds and performance is evaluated on the remaining fold. Performance metrics evaluated during each iteration included the correlation coefficient (R$^2$), root mean squared error (RMSE), and elapsed time during training and inference. After all iterations completed, means and standard deviations of performance metrics were computed to provide a measurement of each model's generalizability. Performance metrics are detailed in @sec:comparing-MADMLMs.

# Results {#sec:results}

## Comparing MAGEMin and Perple_X {#sec:comparing-GFEs}

In practice, small differences in MADs arise as a result of MAGEMin and Perple_X converging on different local minima of GFE (@fig:benchmark-PUM-density). However, typical density differences between MAGEMin and Perple_X on the order of $\leq$ 5% indicate high degrees of internal consistency and correlation between MAGEMin and Perple_X algorithms. The largest deviations between MAGEMin and Perple_X (up to 21% difference) occur far above the liquidus, where Perple_X shows anomalously high-density liquid compared to MAGEMin ([@fig:benchmark-PUM-density]c).

MAGEMin and Perple_X density models are also externally consistent with empirical data compiled in the Preliminary Reference Earth Model [PREM, @dziewonski1981]. Unlike the PREM, however, MAGEMin and Perple_X define a series of discrete density increases between 410 and 660 km ([@fig:benchmark-PUM-density]d).

![PT diagrams in (a, b) show density (in g/cm$^3$) calculated by GFEM programs MAGEMin and Perple_X. The PT diagram in (c) shows the percent difference between MAGEMin and Perple_X density models. Density vs. pressure diagram in (d) shows density changes along a warm mantle geotherm. White lines are the bounding geotherms for subsetting MADMLM training data from @fig:training-pt-range. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps. The PREM model is from @dziewonski1981.](assets/figs/image-PUM-128x128-DensityOfFullAssemblage.png){#fig:benchmark-PUM-density}

## Comparing MADMLMs {#sec:comparing-MADMLMs}

![caption](assets/figs/all-surf-PUM-128x128-DensityOfFullAssemblage.png)

{{ regression-info.md }}
: MADMLM performance measured by 30-fold cross-validation. {#tbl:regression-info}

![caption](assets/figs/regression-metrics.png)

## Comparing MADMLMs with MAGEMin and Perple_X

# Discussion

## Validating MADML Density Models

![Correlation diagrams in (a, b) show error rates between GFEM (targets) and Decision Tree models (predictions). Density vs. pressure diagrams in (b, c) show density changes along a warm mantle geotherm. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps. The PREM model is from @dziewonski1981.](assets/figs/prem-PUM-128x128-DensityOfFullAssemblage-Decision-Tree.png)

# References

<div id="refs"></div>

\cleardoublepage

# Appendix

<!--
## GFEM Benchmarking

Benchmarking GFEM programs was a necessary first step for estimating the time required for building MADMLM training datasets and quantifying the efficiency of incumbent GFEM programs (@fig:benchmark-times), which our MADMLMs will need to beat to be considered an advancement beyond the status-quo. Estimated bulk compositions for primitive and depleted mantle-derived rocks ([@tbl:benchmark-comps]) were used for benchmarking MAGEMin and Perple_X. [@tbl:benchmark-times-table] shows the computation times with respect to various PT grid resolutions (8x8, 16x16, 32x32, 64x64, 128x128). All computations were made on a Macbook Pro (2022; M2 chip) with macOS 13.4 and Python 3.11.4. Note that MAGEMin was ran on 6 CPU cores in parallel, while Perple_X does not have parallel capabilities.

{{ benchmark-times.md }}
: MAD computation times (in seconds) for various bulk mantle compositions. {#tbl:benchmark-times-table}
-->

![PT-density diagrams in (a, b) show density surfaces (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density surfaces in (c, d) are Support Vector models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and Support Vector models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/surf-PUM-128x128-DensityOfFullAssemblage-Support-Vector.png)

![PT diagrams in (a, b) show density distributions (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density distributions in (c, d) are Support Vector models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and Support Vector models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/image-PUM-128x128-DensityOfFullAssemblage-Support-Vector.png)

![PT-density diagrams in (a, b) show density surfaces (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density surfaces in (c, d) are Random Forest models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and Random Forest models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/surf-PUM-128x128-DensityOfFullAssemblage-Random-Forest.png)

![PT diagrams in (a, b) show density distributions (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density distributions in (c, d) are Random Forest models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and Random Forest models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/image-PUM-128x128-DensityOfFullAssemblage-Random-Forest.png)

![PT-density diagrams in (a, b) show density surfaces (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density surfaces in (c, d) are Gradient Boost models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and Gradient Boost models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/surf-PUM-128x128-DensityOfFullAssemblage-Gradient-Boost.png)

![PT diagrams in (a, b) show density distributions (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density distributions in (c, d) are Gradient Boost models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and Gradient Boost models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/image-PUM-128x128-DensityOfFullAssemblage-Gradient-Boost.png)

![PT-density diagrams in (a, b) show density surfaces (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density surfaces in (c, d) are K Nearest models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and K Nearest models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/surf-PUM-128x128-DensityOfFullAssemblage-K-Nearest.png)

![PT diagrams in (a, b) show density distributions (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density distributions in (c, d) are K Nearest models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and K Nearest models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/image-PUM-128x128-DensityOfFullAssemblage-K-Nearest.png)

![PT-density diagrams in (a, b) show density surfaces (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density surfaces in (c, d) are Neural Network 1L models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and Neural Network 1L models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/surf-PUM-128x128-DensityOfFullAssemblage-Neural-Network-1L.png)

![PT diagrams in (a, b) show density distributions (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density distributions in (c, d) are Neural Network 1L models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and Neural Network 1L models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/image-PUM-128x128-DensityOfFullAssemblage-Neural-Network-1L.png)

![PT-density diagrams in (a, b) show density surfaces (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density surfaces in (c, d) are Neural Network 2L models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and Neural Network 2L models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/surf-PUM-128x128-DensityOfFullAssemblage-Neural-Network-2L.png)

![PT diagrams in (a, b) show density distributions (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density distributions in (c, d) are Neural Network 2L models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and Neural Network 2L models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/image-PUM-128x128-DensityOfFullAssemblage-Neural-Network-2L.png)

![PT-density diagrams in (a, b) show density surfaces (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density surfaces in (c, d) are Neural Network 3L models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and Neural Network 3L models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/surf-PUM-128x128-DensityOfFullAssemblage-Neural-Network-3L.png)

![PT diagrams in (a, b) show density distributions (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density distributions in (c, d) are Neural Network 3L models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and Neural Network 3L models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/image-PUM-128x128-DensityOfFullAssemblage-Neural-Network-3L.png)

![PT-density diagrams in (a, b) show density surfaces (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density surfaces in (c, d) are Decision Tree models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and Decision Tree models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/surf-PUM-128x128-DensityOfFullAssemblage-Decision-Tree.png)

![PT diagrams in (a, b) show density distributions (in g/cm$^3$) calulated by GFEM programs MAGEMin and Perplex. Density distributions in (c, d) are Decision Tree models trained on the GFEM models in (a, b). The surfaces in (e, f) show the percent difference between GFEM and Decision Tree models. GFEM programs assume a PUM bulk composition from @tbl:benchmark-comps.](assets/figs/image-PUM-128x128-DensityOfFullAssemblage-Decision-Tree.png)
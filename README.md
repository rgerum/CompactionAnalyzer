# CompactionAnalyzer 

<img src="../master//docs/images/Fig1-rawtostructure.png" width="1000" />

## Quantification of tissue compaction around cells

Python package to quantify the tissue compaction (as a measure of the contractile strength) generated by cells or multicellular spheroids that are embedded in fiber materials. For this we provide the two following approaches:

* Evaluating the directionality of fibers towards the cell center 
* Evaluating the increased intensity around the cell.  


## Installation
The package can be installed by cloning this repository or downloading the repository as a zip file [here](https://github.com/davidbhr/CompactionAnalyzer/zipball/master). For installation, run the following command within the unzipped folder, in which the *setup.py* file is located: `pip install -e .`. This automatically downloads and installs all other required packages.

## Tutorial

The scripts within the turorial folder might be a good start to get familiar with the analyis. The script `CompactionAnalysis_cells_collagen.py` evaluates 4 example cells that are embedded in collagen and compact the surrounding tissue. We recorded the fiber stucture using 2nd harmonic imaging and the cells using fluorescent staining. 

Further scripts `CompactionAnalysis_empty_collagen.py` & `CompactionAnalysis_artificial_data.py` evaluate empty collagen gels that show random fiber allignement and artifiacl data with random allignement. 

We start to import all necessary functions in these scripts using

```python
from CompactionAnalyzer.CompactionFunctions import *
```

For the analysis, we then need per cell an image of the fiber structure (e.g. 2nd harmonic, confocal reflection or stained fluorescence images; maximum intensity projection around the cells might be useful) and an image of the cell for segmentation (staining or brightfield). 

We define the input data for the fibers using `fiber_list_string` ant the cells using `cell_list_string` (here we can utilize the * place holder to selecet multiple images).  `generate_lists()` then searches all specified fiber and cell paths and creates the output subfolder in the specified `output_folder` directory completley automatically.

```python
output_folder = "C:\user\Analysis_output"                     # output folder that will be created and filled automatically
fiber_list_string =  r"C:\user\imagedata\cell_*\*ch00*.tif"   # input fiber images of all cells 
cell_list_string =  r"C:\user\imagedata\cell_*\*ch01*.tif"    # input stained images of all cells 

fiber_list,cell_list, out_list = generate_lists(fiber_list_string, cell_list_string, output_main =output_folder)
```

We now want to start the analysis and compute the orientation of individual fibers using structure tensor analysis. Here *sigma_tensor* is the kernel size that determines the length scale on which the strucutre is analysed. The kernel size should be in the range of the structure-size we want to look at and can be optimized for the individual application. For our fiber gels we use a value of 7 µm, which is in range of the pore size. The script `DetermineWindowSize.py` in the tutorial folder provides a template to systematically test different windowsizes on the same image pair and from that select the ideal size of the `sigma_tensor` for this setup (which displays a peak in the orientation).


We can redefine all of the following paramters before starting the analysis. The corresponding pixel scale is set as `scale` and the segmentiation can be changed by using the `segmention_thres` or by changing the local contrast enhancement via `seg_gaus1, seg_gaus2`. With `show_segmentation = True` we can inspect the segmentation or - if preferred - segment the mask manually by clicking using `manual_segmention  = True`. Further, a maximal distance around the cell center can be specified for the analysis using `max_dist`. 

```python
scale =  0.318                  # imagescale in um per pixel
sigma_tensor = 7/scale          # sigma of applied gauss filter / windowsize for the structure tensor analysis in px
                                # should be in the order of the objects to analyze !! 
                                # 7 um for collagen 
edge = 40                       # Cut off pixels at the edge since values at the border cannot be trusted
segmention_thres = 1.0          # for cell segmentation, thres 1 equals normal otsu threshold , change to detect different percentage of bright pixel
max_dist = None                 # optional: specify the maximal distance around cell center for the analysis (in px)
seg_gaus1, seg_gaus2 = 0.5,100  # 2 gaus filters used as bandpassfilter for local contrast enhancement; For seg_gaus2 = None a single gauss filter is applied
max_dist = None,                # optional: specify the maximal distance around cell center for analysis (in px)
regional_max_correction = True  # background correction using regional maxima approach
show_segmentation = False       # display the segmentation output (script won't run further)
sigma_first_blur  = 0.5         # slight first bluring of whole image before appplying the structure tensor
angle_sections = 5              # size of angle sections in degree 
shell_width =  None             # pixel width of distance shells (px-value=um-value/scale)
manual_segmention = False       # segmentation of mask by manual clicking the cell outline
plotting = True                 # creates and saves individual figures additionally to the excel files 
dpi = 200                       # resolution of figures 
SaveNumpy = False               # saves numpy arrays for later analysis - can create large data files
norm1=1,norm2 = 99              # contrast spreading for input images between norm1- and norm2-percentile; values below norm1-percentile are set to zero and
                                # values above norm2-percentile are set to 1
seg_invert=False                # if segmentation is inverted dark objects are detected inseated of bright objects
seg_iter = 1                    # number of repetitions of  binary closing, dilation and filling holes steps
segmention_method="otsu"        # use "otsu", "entropy" or "yen"  as segmentation method
segmention_min_area = 1000      # small bjects below this px-area are removed during cell segmentation
load_segmentation = False       # if True enter the path of the segementation.npy - file in path_seg
path_seg = None                 # to load a mask
```


Now we can start to analyse all our cells individually using the single function `StuctureAnalysisMain` (follow the scripts in the tutorial folder):

```python
# Start the structure analysis with the above specified parameters
StuctureAnalysisMain(fiber_list=fiber_list,
                     cell_list=cell_list, 
                     out_list=out_list,
                     scale=scale, 
                     sigma_tensor = sigma_tensor , 
                     ...)
```


For each cell we now receive 3 excel files: 

* `results_total.xlsx`    - Evaluating the overall orientation within the field of view 
* `results_distance.xlsx` - Evaluating the orientation & Intensity in distance shells towards the cell surface
* `results_angle.xlsx`    - Evaluating  the orientation & Intensity in angle sections around the cell center

To compare different cells we can utilize e.g the total orientation within a field of view (requires that all cells have the same Field of View) or could also compare the intensity values in the first distance shell(s). 


<img src="../master//docs/images//Fig2-orientationeval.png" width="1000" />


If we now want to evaluate a measurement containing multiple cells, we can read in all excel files (of individual cells) in the underlying folders of the given `data` path and combine them in a new excel file by using:

```python
SummarizeResultsTotal(data="Analysis_output", output_folder= "Analysis_output\Combine_Set1")
SummarizeResultsDistance(data="Analysis_output", output_folder= "Analysis_output\Combine_Set1")
```

 > Note: These function searches all subfolders for the *"results_total.xlsx"* and *"results_distance.xlsx"* files. If you want to discard outliers it might be practical to rename the corresponding files to for example *"_results_total.xlsx"* and *"_results_distance.xlsx"*)


Now we receive a compromised excel sheet that returns the global analysis for all cells and another excel sheet with the mean distance analysis. The different columns `Mean Angle` and `Orientation` refer to the angular deviation between all orientation vectors to the respective cell center and the hereby resulting orientation. These quantities are weighted by the coherency (orientation strength) and additionally also by both, the coherency and the image intensity.  From the different cells we now can calculate different quantities, as for example the mean `Orientation (weighted by intensity and coherency)` of all cells, which is named `Overall weighted Oriantation (mean all cells)` and also stored in the same excel file.


<img src="../master/docs/images/Fig3-combineexcel.png" width="800" />

## Graphical User Interface (GUI)

For an easy use of the CompactionAnalyzer, we provide a graphical user interface (GUI) that simplifies the execution and evaluation of several experiments. To start the GUI, just run the script `GUI.py`. Pairs of fiber and cell images can be loaded individually or batchwise by using the *-placeholder.

<img src="../master//docs/images//GUI_readimages.png" width="800" />

Parameters can be configurated and the cell-segmentationen viewed and changed individually per cell. Upon `Run` the analysis is started and results will be stored in specified output folder.

<img src="../master//docs/images//GUI_evaluation.png" width="800" />

For data analysis, the `results_total.xlsx` files can be loaded again individually or batchwise by using the *-placeholder. Intensity and Orientation can then be evaluated individually or by adding several cells to user defined groups. Bar and distance plots (mean+-se) are created automatically and individual python-scripts to re-plot the data can be exported.

<img src="../master//docs/images//GUI_DataAnalysis.png" width="800" />



## Resolving Drug Effects & Multicellular Compaction Assay

An application of the CompactionAnalyzer is resolving drug-dependend effects on cell contractility. 

Beneath individual cells also the compaction assay can be used on a multicellular level using for example mutlicellular spheroids. This offers the advantage of uniform round shape and less movement so that even a lower sample number might be suffiecient. 


> Additionally, absolute forces of spheroids can be measured using the *jointforces* python package [here](https://github.com/christophmark/jointforces), which requires additonal material measurements & timelapse imaging. Absolute forces of cell can be assesed using *saenopy* [here](https://github.com/rgerum/saenopy), which requires additonal material measurements and two (larger) 3D stacks of the contracted and realaxed state per cell.


## Read more

Read more about the method in the following article

TODO: Write a paper

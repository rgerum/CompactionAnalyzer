# CompactionAnalyzer 

## Quantification of tissue compaction around cells

Python package to quantify the tissue compaction (as a measure of the contractile strength) generated by cells or multicellular spheroids that are embedded in fiber materials. For this we provide the two following approaches:

**A**: Evaluating the directionality of fibers towards the cell center <br>
**B**: Evaluating the increased intensity around the cell.  <br>


## Installation
The package can be installed by cloning this repository or downloading the repository as a zip file [here](https://github.com/davidbhr/CompactionAnalyzer/zipball/master). For installation, run the following command within the unzipped folder, in which the *setup.py* file is located: `pip install -e .`. This automatically downloads and installs all other required packages.

## Tutorial

The script 'CompactionAnalysis.py' within the turorial folder might be good to start to get familiar with the analyis. For the analysis we need per each cell an image of the fiber structure (e.g. 2nd harmonic, confocal reflection or stained fluorescence images; maximum intensity projection around the cells might be useful) and an image of the cell for segmentation (staining or brightfield). 

```python
from CompactionAnalyzer.CompactionFunctions import *
output_folder = "Analysis_output" 
fiber_list_string =  r"..\..\data\stack 2 relocated\pos002\*z6*.tif"
cell_list_string =  r"..\..\data\stack 2 relocated\pos002\*z6*.tif" 

fiber_list,cell_list, out_list = generate_lists(fiber_list_string, cell_list_string, output_main =output_folder)
```

We then compute the orientation of individual fibers using structure tensor analysis. Here *sigma_tensor* is the kernel size that determines the length scale on which the strucutre is analysed. The kernel size should be in the range of structure we want to look at and can be optimized for the individual application. For our fiber gels we use a value of 7 µm, which is in range of the pore size. 


We can redefine all of the following paramters before starting the analysis. The corresponding pixel scale is set as `scale` and the segmentiation can be changed by using the `segmention_thres` or changing the local contrast enhancement via `seg_gaus1, seg_gaus2`. With `show_segmentation = True` we can inspect the segmentation or if preffered segment the mask manually by clicking for `show_segmentation = True`.

```python
scale =  0.318                  # imagescale as um per pixel
sigma_tensor = 7/scale          # sigma of applied gauss filter / window for structure tensor analysis in px
                                # should be in the order of the objects to analyze !! 
                                # 7 um for collagen 
edge = 40                       # Cutt of pixels at the edge since values at the border cannot be trusted
segmention_thres = 1.0          # for cell segemetntion, thres 1 equals normal otsu threshold , change to detect different percentage of bright pixel
seg_gaus1, seg_gaus2 = 8,80     # 2 gaus filters used for local contrast enhancement for segementation
show_segmentation = False        # display the segmentation output to test parameters - script wont run further
sigma_first_blur  = 0.5         # slight first bluring of whole image before using structure tensor
angle_sections = 5              # size of angle sections in degree 
shell_width =  5/scale          # pixel width of distance shells (px-value=um-value/scale)
manual_segmention = False       # manual segmentation of mask by click cell outline
plotting = True                 # creates and saves plots additionally to excel files 
dpi = 200                       # resolution of plots to be stored
SaveNumpy = True                # saves numpy arrays for later analysis - might create lots of data
norm1,norm2 = 1,99              # contrast spreading for input images  by setting all values below norm1-percentile to zero and
                                # all values above norm2-percentile to 1
seg_invert=False                # if segmentation is inverted (True) dark objects are detected inseated of bright ones
seg_iter = 1                    # repetition of closing and dilation steps for segmentation      
segmention_method="otsu"               #  use "otsu" or "yen"  as segmentation method
load_segmentation = False        # if true enter the path of the segementation math in path_seg to
path_seg = None                  # load in a saved.segmetnion.npy 
```

Then we can start the analyis using the single function (follow the full 'CompactionAnalysis.py' script)

```python
# Start the structure analysis with the above specified parameters
StuctureAnalysisMain(fiber_list=fiber_list,
                     cell_list=cell_list, 
                     out_list=out_list,
                     scale=scale, 
                     sigma_tensor = sigma_tensor , 
                     ...)
```








If we have more cells we can easily read in all of them and analyze them individually sin * operator




For ever cell analysis is done for global, angle and distance. Results are stored in individual excel sheets and - if activated - plots




read in and plotted again .. show some data




To evaluate measurements mseveral cells we can combine all data in selected subfolders usin 

...

Resutlng excel files contain the mean data for all cells

Same can be done for distance analysis using
...

Then ...







## Maxprojections

Might be usefull to use Maximum intensity image around cell (smalls stacks) to include maximal compation.  
 For different max projection height it might be necessary to change parameter X , since fiberstructure seems / erscheint more densly. Maximumprojection can also be created using the function   XY


## Multicellular Compaction Assay

Beneath individual cells also the compaction can bes assesed on a multicellular level using for example cell spheoids. This also offers the advantage that uniform round shape here and less moement The compaction can be accesed using the same analysis.

Additionally, absolute forces can be measured using the python package **Jointforces** LINK HERE (requires additonal material measurements & timelapse imaging)

## Resolving compound effects

resolve contractility of tumor spheroids and drug responses.

## How to cite

If you are using the CompactionAnalyzer feel free to cite:

TODO: Write a paper and put it here...

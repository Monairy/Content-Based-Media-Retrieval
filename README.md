# Content-Based-Media-Retrieval  
## To run project, make sure you have Python 3.x installed with following dpendencies   
tkinter:    
  ` pip install tk   `       
matplotlib:       
 `  pip install matplotlib     `       
pillow:   
  ` pip install Pillow==2.2.2    `    
shutil:   
  ` pip install pytest-shutil    `       
numpy:    
 `   pip install numpy   `           
pickle:    
   ` pip install pickle     `         
opencv:       
`    pip install opencv-python     `      
moviepiy:      
  `  pip install moviepy    `           
katna:       
   ` pip install katna   `       


## to run code:
Download the repository and run `app.py`

## to compile into single executable:   
 `$ pyinstaller -F --hidden-import="sklearn.utils._cython_blas" --hidden-import="sklearn.neighbors.typedefs" --hidden-import="sklearn.neighbors.quad_tree" --hidden-import="sklearn.tree._utils" --hidden-import="sklearn.utils._weight_vector" --hidden-import="scipy.special.cython_special" --hidden-import="skimage.filters.rank.core_cy_3d" --onefile app.py   `

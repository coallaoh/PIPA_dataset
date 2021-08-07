# PIPA dataset

It's been a while since the dataset has been published. There has been a request for this dataset yesterday and I realised the dataset is gone!

The pointers to the original dataset and our ICCV'15 splits are as follows:

- https://people.eecs.berkeley.edu/~nzhang/piper.html
- https://www.mpi-inf.mpg.de/departments/computer-vision-and-machine-learning/research/people-detection-pose-estimation-and-tracking/person-recognition-in-personal-photo-collections

They are not working any longer. Please use this Github repository as a guide.

### Crawling images

We only have access to metadata, not the original images. Fortunately, PIPA dataset is built exclusively on Flickr and Flickr images are accessible with the Photo IDs in our metadata. See [all_data.txt](all_data.txt). It shows the full list of annotated person instances in the PIPA dataset. The second column corresponds to the Photo ID for each instance. 

You can crawl the images from Flickr using the Photo IDs. See https://www.flickr.com/services/api/ for details.

On a browser, one may search the images with Photo ID by: https://www.flickr.com/photo.gne?id=<Photo_ID>. 

Example: https://www.flickr.com/photo.gne?id=12990166725

Note that not all images may be available at the moment. I will try to take a snapshot of the dataset soon, after checking up with the license status for the images.

### Structure of the dataset

The whole dataset is split into `train`, `val`, `test`, and `leftover`, with disjoint person identities. They correspond to column 8 in [all_data.txt](all_data.txt) (values 0, 1, 2, 3, respectively). 

The `val` and `test` sets are further divided into two splits (e.g. `val0` and `val1`). `val0` is meant as a person-specific training set ("registering" identities) and `val1` as the evaluation set for each identity. Same goes for `test0` and `test1`.

I know this is complicated.. It's probably better to describe a bit on how people have been using this dataset. People have typically pre-trained their CNNs on the `train` set for generic identities and then trained person-specific multi-class SVM on top of the CNN features using `val0` or `test0` sets. The CNN + SVM are then evaluated on `val1` or `test1`.


### Person annotations

Each person instance is annotated with a head bounding box and an integer ID (same ID for same person).

**Box**: columns 3-6 in [all_data.txt](all_data.txt) in the order (x,y,w,h).

**ID**: column 7 in [all_data.txt](all_data.txt)


### Evaluation

We have introduced four splits (`val0` vs `val1` or `test0` vs `test1`) corresponding to different difficulty levels (different time gaps between training & test images per person). 

**Original**: Train and test a person's appearance on the same days (proposed in the original PIPA).

**Album**: Train a person's appearance in one album, test on the other album.

**Time**: Train a person's appearance in the earliest time range, test on the latest time range (using photo-taken-date metadata).

**Day**: Train and test a person's appearance on different days (manually separated).

You can find the splits in files of the form `split_{train,val}_{original,album,time,day}.txt`. Each file is organized as 

```
<photoset_id> <photo_id> <xmin> <ymin> <width> <height> <identity_id> <subset_id>  <SPLIT(0/1)>
```

Following the PIPA protocol, your identity classifier must be trained on split 0 instances and be tested on split 1 instances. Then, do the same with the split 0 and 1 swapped. For evaluation, take the average of the these performances.



### References

```
@inproceedings{zhang2015beyond,
  title={Beyond frontal faces: Improving person recognition using multiple cues},
  author={Zhang, Ning and Paluri, Manohar and Taigman, Yaniv and Fergus, Rob and Bourdev, Lubomir},
  booktitle={Proceedings of the IEEE conference on computer vision and pattern recognition},
  pages={4804--4813},
  year={2015}
}

@inproceedings{joon2015person,
  title={Person recognition in personal photo collections},
  author={Joon Oh, Seong and Benenson, Rodrigo and Fritz, Mario and Schiele, Bernt},
  booktitle={Proceedings of the IEEE international conference on computer vision},
  pages={3862--3870},
  year={2015}
}
```

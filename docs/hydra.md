# Hydra


## Introduction 
Hydra is a python framework that provides a (not) convenient way to create a hierarchical configuration by compisition and override through config files and command lines. 
This tutorial is designed to hydra in this project as a **end-user** and will not cover it. We refer to the official documentation for more information.


## Structure
all the `.yaml` files are located in the folder `configs/`. Every folder are (unless stated so ) an subconfiguration that will be called to initialize a part of SPT.

## Discover Hydra :
If you want to test by yourself, just create a python script my_app.py and paste this code:
```python
from omegaconf import DictConfig, OmegaConf
import hydra

@hydra.main(version_base=None, config_path=".", config_name="config")
def my_app(cfg):
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```
and create an adequate config.yaml next to this file based on what you want to test.

## Command Line :

### load a configuration:

To load a configuration, simply pass `name_configuration=NAME.yaml` after your script 

example:

```bash
python src/train.py datamodule=s3dis_simulated.yaml
```
will load in cfg.datamodule the .yaml `datamodule/s3dis_simulated.yaml`


example: 
```bash
python src/train.py experiment=train/s3dis_simulated.yaml
```

will load in `cfg.datamodule` the .yaml `experiment/train/s3dis_simulated.yaml`

> **Warning**: if you want to load a configuration nested in another package, you have to specify the relative path with / :
example:
 ```bash
python src/train.py experiment=train/s3dis_simulated.yaml predict=predict_s3dis_sim  predict/transfer_config@predict=s3dis_11g
```
> will load (IN PYTHON) in `cfg.predict.transfer_config` the .yaml `s3dis_11g`. Beware the `/` here. The @ is not important here and will be explained later. 

### Change a parameter:

To change a parameter in some config from command line, just write ` my_parameters=new_value`.

example: 

```bash
python src/train.py experiment=train/s3dis_simulated.yaml datamodule.pc_tiling=2
```


If the parameter is nested, you have to use a dot `.` 

example:

```bash
python src/train.py experiment=train/s3dis_simulated.yaml predict=predict_s3dis predict.on_predictions_parameters.save_pred_dataset_to_cloudpoint=True
```
will change the parameters `save_pred_dataset_to_cloudpoint` in  `cfg.predict.on_predictions_parameters` to  `True`



### Going Further

With the command line, you can do complex interpolation, see [interpolation](https://hydra.cc/docs/advanced/override_grammar/basic/) for more information. For more information , see [see](https://hydra.cc/docs/advanced/override_grammar/basic/) as well.

## From a .yaml file:

A Hydra .yaml files is usually composed of 2 things and one optional things: a defaults_list, a list of parameters and optionally a `@package` at the beginning. 


### the defaults list: 

[It](https://hydra.cc/docs/advanced/defaults_list/) specifies how other .yaml will be interconnected:

example: 
```yaml
defaults:
    - datamodule: s3dis.yaml
    - model: spt-2.yaml
```
will load the `datamodule.s3dis.yaml` in `cfg.datamodule` .

### list of parameters:

After the defaults list, it specify a list of entry of cfg. 


### the ` @`  :
the `@` specify how to build in the hierarchical structure.
If it i at the beginning of a .yaml file, it says that the parameters inside the .yaml will be append in the corresponding package:

example 
```yaml
# @package _global_

test: True
```
will set the key `cfg.test` to True even though it was called as a subconfig. 

For further information, see [here](https://hydra.cc/docs/advanced/overriding_packages/)




## TroobleShoot:

### What is the overrides thing ? 


Sometimes, some config can have the words override before, it is because some package can point to the same key several times, it is quite technical and change ` -datamodule: s3dis.yaml` to `override datamodule:s3dis.yaml` if the error happens, just add or remove override and see what works.


### Why do you have all those @ in some .yaml file:
 It specifies the relative place of a .yaml file in the hierarchical configuration. If you are using these, the intertwin between every configuration can be quite complex and not completely obvious.
 If you want to call a  `.yaml` and hydra cannot  find it , specify the ABSOLUTE path instead of the relative one, this should always works.
 
 example: 
 ```.yaml 
 /predict/transfer_config/default.yaml@_here_
 ```
will load the configuration `/predict/transfer_config/default.yaml` in the configuraton `cfg`. 


If the CI doesn't work and ask to appen some @ , just do it . 
  


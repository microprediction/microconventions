# microconventions

This package codifies conventions adopted at www.MicroPrediction.Org, a kind of AI community garden of sorts. The site effects turnkey short term forecasting and automated reuse of algorithms. See also a series of articles at https://www.linkedin.com/in/petercotton/detail/recent-activity/posts/



![](https://i.imgur.com/yKItXmT.png)


## Tutorials

New video tutorials are available at https://www.microprediction.com/python-1 to help you
get started running crawlers at www.microprediction.com


## Dependencies  

    conventions
        |           
   
    <species_conventions>  horizon_conventions   misc_conventions
           |               |                        |
           --------  sep_conventions  ---------------           

If you participate, it is worth a glance at this little library. It is intended to be readable code documenting some choices made. 

## Stream conventions ([code](https://github.com/microprediction/microconventions/blob/master/microconventions/stream_conventions.py))

Governs which names can be top level streams, as compared with derived streams involving tildes. The main thing to remember is that stream names end in .json

    mystream.json

There is a small chance the author regrets the '.json' (though it keeps open various possibilities). 

## Key conventions ([code](https://github.com/microprediction/microconventions/blob/master/microconventions/key_conventions.py))

Refers to the use of Memorable Unique Identifiers. This code wraps the functionality provided at www.muid.org and the MUID Python Package so that it need not be used directly. There are minor distinctions between MUIDs and write_keys. For one thing, MUIDs are often binary strings whereas write_keys are str. This mixin also provides you with conversions between private write_key's, public hashes of the same using shash() that are referred to as codes sometimes, and the spirit animals suggested by the leading characters of the codes. 

## Value conventions ([code](https://github.com/microprediction/microconventions/blob/master/microconventions/value_conventions.py))

Refers to kinds of values. Generally you will not need to worry about this. A time of writing only scalar float values are the subject of community prediction. However other types of value can be stored and the manner in which this is done can depend on the size. 

## Horizon conventions ([code](https://github.com/microprediction/microconventions/blob/master/microconventions/horizon_conventions.py))

A horizon is a combination of a data stream and a time interval measured in seconds, called a delay. Usually the combination is represented as a string with double colon separator. For example

    70::mystream.json  
    
might reference a 1 minute (roughly) ahead forecast. 
 
## Leaderboard conventions ([code](https://github.com/microprediction/microconventions/blob/master/microconventions/leaderboard_conventions.py))

Names for various types of leaderboards. I don't think it is important to study this but the client library needs it. 

## Stats conventions ([code](https://github.com/microprediction/microconventions/blob/master/microconventions/stats_conventions.py))

Not much here, just some backward compatability for norminv, default abscissa for CDFs and the like. 

## Z-Curve conventions ([code](https://github.com/microprediction/microconventions/blob/master/microconventions/zcurve_conventions.py))

Refers in part to naming conventions for derived streams. For example:

    z1~mystream::70.json

is a data stream generated by computing the community implied z-score of points in the stream mystream.json. A community implied z-score is a z-score computed relative to the distribution implied by everyone's predictions. We need to choose a prediction horizon (delay) to specify this. So this particular example refers to z-scores relative to the short horizon predictions (1 minute ahead of time). On the other hand, 

    z1~mystream::3555.json

would refer to z-scores relative to 1 hour ahead forecasts. 

### Space filling curve conventions ([code](https://github.com/microprediction/microconventions/blob/master/microconventions/zcurve_conventions.py))

The zcurve conventions also specify maps [0,1]^2 -> R and [0,1]^3->R that are used to take pairs and triples of z-scores and create univariate 
data streams. These are space filling curves arrived at by interleaving the digits in the binary representations. In the case of two dimensions this is similar to geohashing. These streams are
denoted as follows: 

    z2~bob~mary::3555.json 
   
refers to embeddings of z-scores from streams bob.json and mary.json. Here is a [video](https://www.swarmprediction.com/zcurves.html) that explains the embedding better than I can.

### Miscellaneous ([code](https://github.com/microprediction/microconventions/blob/master/microconventions/misc_conventions.py))

I dare say some of these might migrate, but the code in misc_conventions provides a collection of naming conventions that you will need to know if you wish to use
the fairly powerful /live API (see https://api.microprediction.org and scroll to "Live"). This API can be used to extract various quantities in the database, not 
all of whom have their own standalone APIs. For example you can get lagged time/value pairs in two ways: 

    https://api.microprediction.org/live/lagged::cop.json
    https://api.microprediction.org/lagged/cop.json
    
however if you really just want the values you can only get it as 

    https://api.microprediction.org/live/lagged_values::cop.json
    
Similarly you can get confirms, warnings, errors, transactions and so on all using /live. This may or may not help if you want to quickly write a client 
in another language. 

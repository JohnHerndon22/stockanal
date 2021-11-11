# hurstexp.py

import pandas as pd
import numpy as np

def HurstEXP( ts = [ None, ] ):   # TESTED: HurstEXP() Hurst exponent ( Browninan Motion & other observations measure ) 100+ BARs back(!)
            """                                                         __doc__
            USAGE:
                        HurstEXP( ts = [ None, ] )

                        Returns the Hurst Exponent of the time series vector ts[]

            PARAMETERS:
                        ts[,]   a time-series, with 100+ elements
                                ( or [ None, ] that produces a demo run )

            RETURNS:
                        float - a Hurst Exponent approximation,
                                as a real value
                                or
                                an explanatory string on an empty call
            THROWS:
                        n/a
            EXAMPLE:
                        >>> HurstEXP()                                        # actual numbers will vary, as per np.random.randn() generator used
                        HurstEXP( Geometric Browian Motion ):    0.49447454
                        HurstEXP(    Mean-Reverting Series ):   -0.00016013
                        HurstEXP(          Trending Series ):    0.95748937
                        'SYNTH series demo ( on HurstEXP( ts == [ None, ] ) ) # actual numbers vary, as per np.random.randn() generator'

                        >>> HurstEXP( rolling_window( aDSEG[:,idxC], 100 ) )
            REF.s:
                        >>> www.quantstart.com/articles/Basics-of-Statistical-Mean-Reversion-Testing
            """
            #---------------------------------------------------------------------------------------------------------------------------<self-reflective>
            if ( ts[0] == None ):                                       # DEMO: Create a SYNTH Geometric Brownian Motion, Mean-Reverting and Trending Series:

                 gbm = np.log( 1000 + np.cumsum(     np.random.randn( 100000 ) ) )  # a Geometric Brownian Motion[log(1000 + rand), log(1000 + rand + rand ), log(1000 + rand + rand + rand ),... log(  1000 + rand + ... )]
                 mr  = np.log( 1000 +                np.random.randn( 100000 )   )  # a Mean-Reverting Series    [log(1000 + rand), log(1000 + rand        ), log(1000 + rand               ),... log(  1000 + rand       )]
                 tr  = np.log( 1000 + np.cumsum( 1 + np.random.randn( 100000 ) ) )  # a Trending Series          [log(1001 + rand), log(1002 + rand + rand ), log(1003 + rand + rand + rand ),... log(101000 + rand + ... )]

                                                                        # Output the Hurst Exponent for each of the above SYNTH series
                 print ( "HurstEXP( Geometric Browian Motion ):   {0: > 12.8f}".format( HurstEXP( gbm ) ) )
                 print ( "HurstEXP(    Mean-Reverting Series ):   {0: > 12.8f}".format( HurstEXP( mr  ) ) )
                 print ( "HurstEXP(          Trending Series ):   {0: > 12.8f}".format( HurstEXP( tr  ) ) )

                 return ( "SYNTH series demo ( on HurstEXP( ts == [ None, ] ) ) # actual numbers vary, as per np.random.randn() generator" )

            pass;     too_short_list = 101 - len( ts )                  # MUST HAVE 101+ ELEMENTS
            if ( 0 <  too_short_list ):                                 # IF NOT:
                 ts = too_short_list * ts[:1] + ts                      #    PRE-PEND SUFFICIENT NUMBER of [ts[0],]-as-list REPLICAS TO THE LIST-HEAD
            #---------------------------------------------------------------------------------------------------------------------------
            lags = range( 2, 100 )                                                              # Create the range of lag values
            tau  = [ np.sqrt( np.std( np.subtract( ts[lag:], ts[:-lag] ) ) ) for lag in lags ]  # Calculate the array of the variances of the lagged differences
            #oly = np.polyfit( np.log( lags ), np.log( tau ), 1 )                               # Use a linear fit to estimate the Hurst Exponent
            #eturn ( 2.0 * poly[0] )                                                            # Return the Hurst exponent from the polyfit output

            return ( 2.0 * np.polyfit( np.log( lags ), np.log( tau ), 1 )[0] )                  # Return the Hurst exponent from the polyfit output ( a linear fit to estimate the Hurst Exponent )


df = pd.read_csv('SSO_price.csv')
[ ( -i, HurstEXP( ts = df['Close'][:-i] ) ) for i in range( 1, 200 ) ] # should call the HurstEXP for the last 200 days

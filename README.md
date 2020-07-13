# vrn-cntrd-simulator
A simulator to implement and test a robot deployment pattern using the Voronoi-Centroid (VRN-CNTRD) algorithm

Original research paper: http://motion.me.ucsb.edu/pdf/2002j-cmkb.pdf

Built using Python 3.7.7 <br />
Install all the dependencies using the provided requirements.txt file

### To run the simulator
<pre><code> python Simulator </pre></code>

### To modify the environment
The module receives the parameters from the <i>config.json</i> file inside the <b>Simulator</b> directory. You can use that template to make your own <i>config.json</i> file. You can inject it as follows
<pre><code> python Simulator --config <i>path/to/config/file</i> </pre></code>

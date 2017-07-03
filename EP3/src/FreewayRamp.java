import java.awt.Graphics;
import java.lang.reflect.Array;
import java.util.Arrays;

import org.opensourcephysics.display.*;
import org.opensourcephysics.frames.*;
import org.opensourcephysics.display2d.*;
import org.opensourcephysics.controls.*;

public class FreewayRamp implements Drawable{

    public int t, steps, roadLength, numberOfCars, maximumVelocity;
    public int scrollTime=100;
    public double flow, p, p2; //probability of reducing velocity
    public int[] v, x, xtemp, state;
    public LatticeFrame spaceTime;
    public double[] distribution;
    private CellLattice road;

    //number of iterations before scrolling space-time diagram

    public void initialize(LatticeFrame spaceTime) {
        this.spaceTime = spaceTime;

        x = new int[numberOfCars];
        xtemp = new int[numberOfCars]; //used to allow parallel updating
        v = new int[numberOfCars];
        state = new int[numberOfCars];
        
        spaceTime.resizeLattice(roadLength, 100);

        road = new CellLattice(roadLength, 3);
        road.setIndexedColor(-1, java.awt.Color.WHITE);
        road.setIndexedColor(0, java.awt.Color.RED);
        road.setIndexedColor(1, java.awt.Color.GREEN);


        for(int i=0; i < roadLength*3/4; i++) {
            road.setValue(roadLength - (i + 1), 2, (byte) -1);
            road.setValue(i, 0, (byte) -1);
        }

        spaceTime.setIndexedColor(0, java.awt.Color.RED);
        spaceTime.setIndexedColor(1, java.awt.Color.GREEN);

        for (int i = 0; i < numberOfCars; i++) {
            x[i] = i;
            state[i] = 1;
            v[i] = Math.random() < 0.5 ? 0 : 1;
        }
        state[0] = 2;

        flow = 0;
        steps = 0;
        t = 0;

    }

    public void step() {

        for(int i = 0; i < numberOfCars; i++) {
            xtemp[i] = x[i];
        }

        for(int i = 0; i<numberOfCars; i++) {
            if(v[i]<maximumVelocity)
                v[i]++; //acceleration

            //distance between cars
            int d = roadLength;
            int mincar = 0;
            for (int c = 0; c < numberOfCars; c++) {
                if (state[i] == state[c]) {
                    if (xtemp[i] < xtemp[c] && xtemp[c] - xtemp[i] < d)
                        d = xtemp[c] - xtemp[i];
                    if (xtemp[c] < xtemp[mincar])
                        mincar = c;
                }
            }

            if (state[i] == 2 && roadLength/4 - xtemp[i] + 1 < d)
                d = roadLength/4 - xtemp[i] + 1;

            //periodic boundary conditions, d = 0 correctly treats one
            //car on road
            if(d <= 0) d+=roadLength;

            if(v[i]>=d)
                v[i]=d-1; //slow down due to cars in front

            if((v[i] > 0) && (Math.random() < p))
                v[i]--; //randomization

            x[i]=(xtemp[i]+v[i])%roadLength;
            if (x[i] < roadLength/4 && state[i] == 0)
                state[i] = 2;

            if (state[i] == 2 && x[i] == roadLength/4) {
                boolean can = true;
                for (int c = 0; c < numberOfCars; c++)
                    if (x[c] == x[i] && i != c)
                        can = false;
                if (can)
                    state[i] = 1;
            }
            if (state[i] == 1 && x[i] == roadLength*3/4) {
                boolean can = true;
                for (int c = 0; c < numberOfCars; c++)
                    if (x[c] == x[i] && i != c)
                        can = false;
                if (can && Math.random() < p2)
                    state[i] = 0;
            }
            flow += v[i];

        }

        steps++;
        computeSpaceTimeDiagram();
    }

    public void computeSpaceTimeDiagram() {
        t++;
        
        if(t<scrollTime)
            for(int i = 0; i < numberOfCars; i++)
                spaceTime.setValue(x[i], t, 1);

        else {
            for(int y = 0; y < scrollTime-1; y++)
                for(int i = 0; i < roadLength; i++)
                    spaceTime.setValue(i, y, spaceTime.getValue(i, y+1));

            for(int i = 0; i < roadLength; i++)
                spaceTime.setValue(i, scrollTime-1, 0); //zero last row

            for(int i=0;i<numberOfCars;i++)
                spaceTime.setValue(x[i], scrollTime-1, 1); //add new row
        }
    }

    public void computeHistogram(LatticeFrame frame, int[] distribution, int maxy) {
        for (int i = 0; i < distribution.length; i++) {
            for (int j = 0; j < maxy; j++) {
                if (distribution[i] <= j)
                    frame.setValue(i, j, 0);
                else
                    frame.setValue(i, j, 1);
            }
        }
    }

    public void draw(DrawingPanel panel, Graphics g) {
        if(x==null) return;
        
        road.setBlock(0, 0, new byte[roadLength][1]);
        road.setBlock(0, 1, new byte[roadLength][1]);
        road.setBlock(0, 2, new byte[roadLength][1]);

        for(int i=0; i < roadLength*3/4; i++) {
            road.setValue(roadLength - (i + 1), 2, (byte) -1);
            road.setValue(i, 0, (byte) -1);
        }

        for(int i=0; i < numberOfCars; i++)
            road.setValue(x[i], state[i], (byte) 1);

        road.draw(panel, g);
        g.drawString("NumberofSteps=" + steps, 10, 20);
        g.drawString("Flow=" + ControlUtils.f3((double)flow/(roadLength*steps)), 10, 40);
        g.drawString("Density=" + ControlUtils.f3((double)numberOfCars/(roadLength)), 10, 60);
    }
}

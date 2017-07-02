import java.awt.Graphics;
import java.lang.reflect.Array;
import java.util.Arrays;

import org.opensourcephysics.display.*;
import org.opensourcephysics.frames.*;
import org.opensourcephysics.display2d.*;
import org.opensourcephysics.controls.*;

public class Freeway2Lane implements Drawable{

    public int t, steps, roadLength, numberOfCars, maximumVelocity;
    public int scrollTime=100;
    public double flow, p; //probability of reducing velocity
    public int[] v, x, lane, xtemp;
    public LatticeFrame spaceTime;
    public double[] distribution;
    private CellLattice road;

    //number of iterations before scrolling space-time diagram

    public void initialize(LatticeFrame spaceTime) {
        this.spaceTime = spaceTime;

        x = new int[numberOfCars];
        lane = new int[numberOfCars];
        xtemp = new int[numberOfCars]; //used to allow parallel updating
        v = new int[numberOfCars];

        spaceTime.resizeLattice(roadLength, 100);

        road = new CellLattice(roadLength, 2);
        road.setIndexedColor(0, java.awt.Color.RED);
        road.setIndexedColor(1, java.awt.Color.GREEN);

        spaceTime.setIndexedColor(0, java.awt.Color.RED);
        spaceTime.setIndexedColor(1, java.awt.Color.GREEN);

        int d = roadLength/numberOfCars;

        x[0] = 0;
        v[0] = maximumVelocity;

        for (int i = 1; i < numberOfCars; i++) {
            x[i] = x[i-1] + d;
            lane[i] = Math.random() < 0.5 ? 0 : 1;
            v[i] = Math.random() < 0.5 ? 0 : 1;
        }

        flow = 0;
        steps = 0;
        t = 0;

    }

    public void step() {

        for(int i = 0; i < numberOfCars; i++)
            xtemp[i] = x[i];

        for(int i = 0; i<numberOfCars; i++) {
            if(v[i]<maximumVelocity)
                v[i]++; //acceleration

            boolean wantToChangeLane = false;
            //distance between cars
            int d = roadLength;
            int mincar = 0;
            for (int c = 0; c < numberOfCars; c++) {
                if (lane[i] == lane[c]) {
                    if (xtemp[i] < xtemp[c] && xtemp[c] - xtemp[i] < d)
                        d = xtemp[c] - xtemp[i];
                    if (xtemp[c] < xtemp[mincar])
                        mincar = c;
                    if (lane[i] == 1 && xtemp[c] == xtemp[i] - 1)
                        wantToChangeLane = true;
                }
            }

            if (d == roadLength)
                d = xtemp[mincar] - xtemp[i] + roadLength;

            if (v[i]>=d) {
                if (lane[i] == 0) wantToChangeLane = true;
                v[i] = d - 1; //slow down due to cars in front
            }

            if ((v[i] > 0) && (Math.random() < p))
                v[i]--; //randomization

            x[i]=(xtemp[i]+v[i])%roadLength;
            if (wantToChangeLane) {
                int changeTo = lane[i] == 0 ? 1 : 0;
                boolean canChange = true;
                for (int c = 0; c < numberOfCars; c++)
                    if (xtemp[c] == x[i])
                        canChange = false;

                if (canChange) {
                    //System.out.println("Car " + i + " changed to lane " + changeTo);
                    lane[i] = changeTo;
                }
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

    public void draw(DrawingPanel panel, Graphics g) {
        if(x==null) return;

        road.setBlock(0, 0, new byte[roadLength][2]);

        for(int i=0; i < numberOfCars; i++)
            road.setValue(x[i], lane[i], (byte) 1);

        road.draw(panel, g);
        g.drawString("NumberofSteps=" + steps, 10, 20);
        g.drawString("Flow=" + ControlUtils.f3((double)flow/(roadLength*steps)), 10, 40);
        g.drawString("Density=" + ControlUtils.f3((double)numberOfCars/(roadLength)), 10, 60);
    }
}

import java.awt.*;
import java.lang.reflect.Array;
import java.util.Arrays;

import org.opensourcephysics.display.*;
import org.opensourcephysics.frames.*;
import org.opensourcephysics.display2d.*;
import org.opensourcephysics.controls.*;

public class Freeway2LaneTruck implements Drawable{

    public int t, steps, roadLength, numberOfAutos;
    public int scrollTime=100;
    public double flow, p; //probability of reducing velocity
    public int[] v, x, lane, xtemp, type, numberOfType, maxVelOfType;
    public double[] flows, vels;
    public LatticeFrame spaceTime;
    public LatticeFrame carVelDist;
    public LatticeFrame truckVelDist;
    public LatticeFrame gapDist;
    public double[] distribution;
    private CellLattice road;

    //number of iterations before scrolling space-time diagram

    public void initialize(LatticeFrame spaceTime, LatticeFrame carDist, LatticeFrame truckDist, LatticeFrame gapDist) {
        this.spaceTime = spaceTime;
        carVelDist = carDist;
        truckVelDist = truckDist;
        this.gapDist = gapDist;

        x = new int[numberOfAutos];
        lane = new int[numberOfAutos];
        type = new int[numberOfAutos];
        xtemp = new int[numberOfAutos]; //used to allow parallel updating
        v = new int[numberOfAutos];
        vels = new double[numberOfType.length];

        spaceTime.resizeLattice(roadLength, 100);

        road = new CellLattice(roadLength, 2);
        road.setIndexedColor(0, java.awt.Color.RED);
        road.setIndexedColor(1, java.awt.Color.GREEN);
        road.setIndexedColor(2, Color.BLUE);

        spaceTime.setIndexedColor(0, Color.RED);
        spaceTime.setIndexedColor(1, Color.GREEN);
        spaceTime.setIndexedColor(2, Color.BLUE);

        carDist.resizeLattice(maxVelOfType[0] + 1, numberOfType[0]);
        carDist.setIndexedColor(0, java.awt.Color.RED);
        carDist.setIndexedColor(1, java.awt.Color.GREEN);

        truckDist.resizeLattice(maxVelOfType[1] + 1, numberOfType[1]);
        truckDist.setIndexedColor(0, java.awt.Color.RED);
        truckDist.setIndexedColor(1, Color.BLUE);

        gapDist.resizeLattice(roadLength, numberOfAutos);
        gapDist.setIndexedColor(0, java.awt.Color.RED);
        gapDist.setIndexedColor(1, java.awt.Color.GREEN);

        x[0] = 0;
        v[0] = 0;

        for (int i = 1; i < numberOfAutos; i++) {
            x[i] = i;
            lane[i] = Math.random() < 0.5 ? 0 : 1;
            v[i] = Math.random() < 0.5 ? 0 : 1;
        }

        int cnt = 0;
        flows = new double[numberOfType.length];
        for (int tp = 0; tp < numberOfType.length; tp++) {
            for (int i = 0; i < numberOfType[tp]; i++)
                type[cnt++] = tp + 1;
        }

        flow = 0;
        for (int i = 0; i < flows.length; i++)
            flows[i] = 0;
        steps = 0;
        t = 0;

    }

    public void step() {

        for(int i = 0; i < numberOfAutos; i++)
            xtemp[i] = x[i];

        for(int i = 0; i < numberOfAutos; i++) {
            if(v[i] < maxVelOfType[type[i] - 1])
                v[i]++; //acceleration

            boolean wantToChangeLane = false;
            //distance between cars
            int d = roadLength;
            int mincar = 0;
            for (int c = 0; c < numberOfAutos; c++) {
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
                for (int c = 0; c < numberOfAutos; c++)
                    if (xtemp[c] == x[i])
                        canChange = false;

                if (canChange) {
                    //System.out.println((type[i] == 1 ? "Car" : "Truck") + " " + i + " changed to lane " + changeTo);
                    lane[i] = changeTo;
                }
            }
            flow += v[i];
            flows[type[i] - 1] += v[i];
        }

        steps++;
        computeSpaceTimeDiagram();
        computeHistogram(carVelDist, getVelocitiesDistribution(1), numberOfType[0]);
        computeHistogram(truckVelDist, getVelocitiesDistribution(2), numberOfType[1]);
        computeHistogram(gapDist, getGapDistribution(), numberOfAutos);
    }

    public void computeSpaceTimeDiagram() {
        t++;

        if(t<scrollTime)
            for(int i = 0; i < numberOfAutos; i++)
                spaceTime.setValue(x[i], t, type[i]);

        else {
            for(int y = 0; y < scrollTime-1; y++)
                for(int i = 0; i < roadLength; i++)
                    spaceTime.setValue(i, y, spaceTime.getValue(i, y+1));

            for(int i = 0; i < roadLength; i++)
                spaceTime.setValue(i, scrollTime-1, 0); //zero last row

            for(int i=0;i<numberOfAutos;i++)
                spaceTime.setValue(x[i], scrollTime-1, type[i]); //add new row
        }
    }

    public int[] getVelocitiesDistribution(int type) {
        int[] distribution = new int[maxVelOfType[type - 1] + 1];
        for (int i = 0; i < maxVelOfType[type - 1]; i++)
            distribution[i] = 0;

        for (int i = 0; i < numberOfAutos; i++)
            if (this.type[i] == type)
                distribution[v[i]] ++;

        return distribution;
    }

    public int[] getGapDistribution() {
        int[] distribution = new int[roadLength];

        for (int i = 0; i < numberOfAutos; i++) {
            int d = roadLength;
            for (int c = 0; c < numberOfAutos; c++) {
                if (lane[i] == lane[c] && i != c) {
                    int tmp = x[c] - x[i];
                    if (x[i] > x[c] && x[c] - x[i] < d)
                        tmp += roadLength;
                    if (tmp < d)
                        d = tmp;
                }
            }

            distribution[d]++;
        }

        return distribution;
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

    public void calcAvgSpeed() {
        for (int i = 0; i < numberOfType.length; i++)
            vels[i] = 0;

        for (int i = 0; i < numberOfAutos; i++)
            vels[type[i] - 1] += v[i];

        for (int i = 0; i < numberOfType.length; i++)
            vels[i] /= numberOfType[i];
    }

    public void draw(DrawingPanel panel, Graphics g) {
        if(x==null) return;

        road.setBlock(0, 0, new byte[roadLength][2]);

        for(int i=0; i < numberOfAutos; i++)
            road.setValue(x[i], lane[i], (byte) type[i]);

        road.draw(panel, g);
        g.drawString("NumberofSteps=" + steps, 10, 20);
        g.drawString("Flow=" + ControlUtils.f3((double)flow/(roadLength*steps)), 10, 40);
        g.drawString("Car flow=" + ControlUtils.f3((double)flows[0]/(roadLength*steps)), 10, 60);
        g.drawString("Truck flow=" + ControlUtils.f3((double)flows[1]/(roadLength*steps)), 10, 80);
        g.drawString("Density=" + ControlUtils.f3((double)numberOfAutos/(roadLength)), 10, 100);
        calcAvgSpeed();
        g.drawString("Car speed=" + ControlUtils.f3(vels[0]), 10, 120);
        g.drawString("Truck speed=" + ControlUtils.f3(vels[1]), 10, 140);
    }
}

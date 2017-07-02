package org.opensourcephysics.sip.ch14.traffic;
import java.awt.Graphics;
import org.opensourcephysics.display.*;
import org.opensourcephysics.frames.*;
import org.opensourcephysics.display2d.*;
import org.opensourcephysics.controls.*;

public class Freeway implements Drawable{

    public int t, steps, roadLength, numberOfCars, maximumVelocity;
    public int scrollTime=100;
    public double flow, p; //probability of reducing velocity
    public int[] v, x, xtemp;
    public LatticeFrame spaceTime;
    public double[] distribution;
    private CellLattice road;

    //number of iterations before scrolling space-time diagram

    public void initialize(LatticeFramespace Time){
        this.spaceTime = spaceTime;
        x = new int[numberOfCars];
        xtemp = new int[numberOfCars]; //used to allow parallel updating
        v = new int[numberOfCars];
        
        spaceTime.resizeLattice(roadLength, 100);
        road = new CellLattice(roadLength, 1);
        road.setIndexedColor(0, java.awt.Color.RED);
        road.setIndexedColor(1, java.awt.Color.GREEN);
        spaceTime.setIndexedColor(0, java.awt.Color.RED);
        spaceTime.setIndexedColor(1, java.awt.Color.GREEN);

        int d = roadLength/numberOfCars;

        x[0] = 0;
        v[0] = maximumVelocity;

        for (inti = 1; i < numberOfCars; i++) {
            x[i] = x[i-1] + d;
            v[i] = Math.random() < 0.5 ? 0 : 1;
        }

        flow = 0;
        steps = 0;
        t = 0;

    }

    public void step(){

        for(int i = 0; i < numberOfCars; i++)
            xtemp[i] = x[i];

        for(int i = 0; i<numberOfCars; i++) {
            if(v[i]<maximumVelocity)
                v[i]++; //acceleration

            //distance between cars
            int d = xtemp[(i+1)%numberOfCars] - xtemp[i];

            //periodic boundary conditions, d = 0 correctly treats one
            //caronroad
            if(d <= 0) d+=roadLength;

            if(v[i]>=d)
                v[i]=d-1; //slow down due to cars in front

            if((v[i] > 0) && (Math.random() < p))
                v[i]--; //randomization

            x[i]=(xtemp[i]+v[i])%roadLength;
            flow += v[i];

        }

        steps++;
        computeSpaceTimeDiagram();
    }

    public void computeSpaceTimeDiagram(){
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
        
        road.setBlock(0, 0, newbyte[roadLength][1]);

        for(int i=0; i < numberOfCars; i++)
            road.setValue(x[i], 0, (byte) 1);

        road.draw(panel, g);
        g.drawString("NumberofSteps=" + steps, 10, 20);
        g.drawString("Flow=" + ControlUtils.f3((double)flow/(roadLength*steps)), 10, 40);
        g.drawString("Density=" + ControlUtils.f3((double)numberOfCars/(roadLength)), 10, 60);
    }
}

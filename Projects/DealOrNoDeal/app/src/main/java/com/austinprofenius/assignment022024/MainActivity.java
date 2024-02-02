package com.austinprofenius.assignment022024;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;

public class MainActivity extends AppCompatActivity {
    ArrayList<ArrayList<Object>> arrayListOfArrayLists = new ArrayList<>();
    ArrayList<Integer> openedCases = new ArrayList<Integer>();
    ArrayList<Integer> unopenedCases = new ArrayList<>();
    ImageView caseclosed1, caseclosed2, caseclosed3,
            caseclosed4, caseclosed5, caseclosed6,
            caseclosed7, caseclosed8, caseclosed9, caseclosed10;
    ImageView imageView1, imageView10, imageView50,
            imageView100, imageView300, imageView1000,
            imageView10000, imageView50000, imageView100000, imageView500000;
    Button buttonDeal, buttonNoDeal, buttonReset;
    int openCaseCount;

    TextView textView;
    double currentOffer;
    int[] caseClosedIds = {
            R.id.caseclosed1, R.id.caseclosed2, R.id.caseclosed3,
            R.id.caseclosed4, R.id.caseclosed5, R.id.caseclosed6,
            R.id.caseclosed7, R.id.caseclosed8, R.id.caseclosed9,
            R.id.caseclosed10
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        int open1 = getResources().getIdentifier("suitcase_open_1", "drawable", getPackageName());
        int open10 = getResources().getIdentifier("suitcase_open_10", "drawable", getPackageName());
        int open50 = getResources().getIdentifier("suitcase_open_50", "drawable", getPackageName());
        int open100 = getResources().getIdentifier("suitcase_open_100", "drawable", getPackageName());
        int open300 = getResources().getIdentifier("suitcase_open_300", "drawable", getPackageName());
        int open1000 = getResources().getIdentifier("suitcase_open_1000", "drawable", getPackageName());
        int open10000 = getResources().getIdentifier("suitcase_open_10000", "drawable", getPackageName());
        int open50000 = getResources().getIdentifier("suitcase_open_50000", "drawable", getPackageName());
        int open100000 = getResources().getIdentifier("suitcase_open_100000", "drawable", getPackageName());
        int open500000 = getResources().getIdentifier("suitcase_open_500000", "drawable", getPackageName());

        int reward1 = getResources().getIdentifier("reward_open_1", "drawable", getPackageName());
        int reward10 = getResources().getIdentifier("reward_open_10", "drawable", getPackageName());
        int reward50 = getResources().getIdentifier("reward_open_50", "drawable", getPackageName());
        int reward100 = getResources().getIdentifier("reward_open_100", "drawable", getPackageName());
        int reward300 = getResources().getIdentifier("reward_open_300", "drawable", getPackageName());
        int reward1000 = getResources().getIdentifier("reward_open_1000", "drawable", getPackageName());
        int reward10000 = getResources().getIdentifier("reward_open_10000", "drawable", getPackageName());
        int reward50000 = getResources().getIdentifier("reward_open_50000", "drawable", getPackageName());
        int reward100000 = getResources().getIdentifier("reward_open_100000", "drawable", getPackageName());
        int reward500000 = getResources().getIdentifier("reward_open_500000", "drawable", getPackageName());

        buttonDeal = findViewById(R.id.buttonDeal);
        buttonNoDeal = findViewById(R.id.buttonNoDeal);
        buttonReset = findViewById(R.id.buttonReset);
        buttonNoDeal.setVisibility(View.INVISIBLE);
        buttonDeal.setVisibility(View.INVISIBLE);

        caseclosed1 = findViewById(R.id.caseclosed1);
        caseclosed2 = findViewById(R.id.caseclosed2);
        caseclosed3 = findViewById(R.id.caseclosed3);
        caseclosed4 = findViewById(R.id.caseclosed4);
        caseclosed5 = findViewById(R.id.caseclosed5);
        caseclosed6 = findViewById(R.id.caseclosed6);
        caseclosed7 = findViewById(R.id.caseclosed7);
        caseclosed8 = findViewById(R.id.caseclosed8);
        caseclosed9 = findViewById(R.id.caseclosed9);
        caseclosed10 = findViewById(R.id.caseclosed10);

        imageView1 = findViewById(R.id.imageView1);
        imageView10 = findViewById(R.id.imageView10);
        imageView50 = findViewById(R.id.imageView50);
        imageView100 = findViewById(R.id.imageView100);
        imageView300 = findViewById(R.id.imageView300);
        imageView1000 = findViewById(R.id.imageView1000);
        imageView10000 = findViewById(R.id.imageView10000);
        imageView50000 = findViewById(R.id.imageView50000);
        imageView100000 = findViewById(R.id.imageView100000);
        imageView500000 = findViewById(R.id.imageView500000);

        textView = findViewById(R.id.textView);

        unopenedCases.add(1);
        unopenedCases.add(10);
        unopenedCases.add(50);
        unopenedCases.add(100);
        unopenedCases.add(300);
        unopenedCases.add(1000);
        unopenedCases.add(10000);
        unopenedCases.add(50000);
        unopenedCases.add(100000);
        unopenedCases.add(500000);

        //int, int drawable res, int drawable res, imageView
        arrayListOfArrayLists.add(createArrayList(1, open1, reward1, imageView1));
        arrayListOfArrayLists.add(createArrayList(10, open10, reward10, imageView10));
        arrayListOfArrayLists.add(createArrayList(50, open50, reward50, imageView50));
        arrayListOfArrayLists.add(createArrayList(100, open100, reward100, imageView100));
        arrayListOfArrayLists.add(createArrayList(300, open300, reward300, imageView300));
        arrayListOfArrayLists.add(createArrayList(1000, open1000, reward1000, imageView1000));
        arrayListOfArrayLists.add(createArrayList(10000, open10000, reward10000, imageView10000));
        arrayListOfArrayLists.add(createArrayList(50000, open50000, reward50000, imageView50000));
        arrayListOfArrayLists.add(createArrayList(100000, open100000, reward100000, imageView100000));
        arrayListOfArrayLists.add(createArrayList(500000, open500000, reward500000, imageView500000));

        Collections.shuffle(arrayListOfArrayLists);

        textView.setText("Choose 4 Cases");

        caseclosed1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openCaseCount++;
                openedCases.add((Integer) arrayListOfArrayLists.get(0).get(0));
                caseclosed1.setImageResource((Integer) arrayListOfArrayLists.get(0).get(1));
                unopenedCases.remove(arrayListOfArrayLists.get(0).get(0));
                ImageView imgView = (ImageView) arrayListOfArrayLists.get(0).get(3);
                imgView.setImageResource((Integer)arrayListOfArrayLists.get(0).get(2));
                checkCases();
            }
        });
        caseclosed2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openCaseCount++;
                openedCases.add((Integer) arrayListOfArrayLists.get(1).get(0));
                caseclosed2.setImageResource((Integer) arrayListOfArrayLists.get(1).get(1));
                unopenedCases.remove(arrayListOfArrayLists.get(1).get(0));
                ImageView imgView = (ImageView) arrayListOfArrayLists.get(1).get(3);
                imgView.setImageResource((Integer)arrayListOfArrayLists.get(1).get(2));
                checkCases();
            }
        });
        caseclosed3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openCaseCount++;
                openedCases.add((Integer) arrayListOfArrayLists.get(2).get(0));
                caseclosed3.setImageResource((Integer) arrayListOfArrayLists.get(2).get(1));
                unopenedCases.remove(arrayListOfArrayLists.get(2).get(0));
                ImageView imgView = (ImageView) arrayListOfArrayLists.get(2).get(3);
                imgView.setImageResource((Integer)arrayListOfArrayLists.get(2).get(2));
                checkCases();
            }
        });
        caseclosed4.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openCaseCount++;
                openedCases.add((Integer) arrayListOfArrayLists.get(3).get(0));
                caseclosed4.setImageResource((Integer) arrayListOfArrayLists.get(3).get(1));
                unopenedCases.remove(arrayListOfArrayLists.get(3).get(0));
                ImageView imgView = (ImageView) arrayListOfArrayLists.get(3).get(3);
                imgView.setImageResource((Integer)arrayListOfArrayLists.get(3).get(2));
                checkCases();
            }
        });
        caseclosed5.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openCaseCount++;
                openedCases.add((Integer) arrayListOfArrayLists.get(4).get(0));
                caseclosed5.setImageResource((Integer) arrayListOfArrayLists.get(4).get(1));
                unopenedCases.remove(arrayListOfArrayLists.get(4).get(0));
                ImageView imgView = (ImageView) arrayListOfArrayLists.get(4).get(3);
                imgView.setImageResource((Integer)arrayListOfArrayLists.get(4).get(2));
                checkCases();
            }
        });
        caseclosed6.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openCaseCount++;
                openedCases.add((Integer) arrayListOfArrayLists.get(5).get(0));
                caseclosed6.setImageResource((Integer) arrayListOfArrayLists.get(5).get(1));
                unopenedCases.remove(arrayListOfArrayLists.get(5).get(0));
                ImageView imgView = (ImageView) arrayListOfArrayLists.get(5).get(3);
                imgView.setImageResource((Integer)arrayListOfArrayLists.get(5).get(2));
                checkCases();
            }
        });
        caseclosed7.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openCaseCount++;
                openedCases.add((Integer) arrayListOfArrayLists.get(6).get(0));
                caseclosed7.setImageResource((Integer) arrayListOfArrayLists.get(6).get(1));
                unopenedCases.remove(arrayListOfArrayLists.get(6).get(0));
                ImageView imgView = (ImageView) arrayListOfArrayLists.get(6).get(3);
                imgView.setImageResource((Integer)arrayListOfArrayLists.get(6).get(2));
                checkCases();
            }
        });
        caseclosed8.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openCaseCount++;
                openedCases.add((Integer) arrayListOfArrayLists.get(7).get(0));
                caseclosed8.setImageResource((Integer) arrayListOfArrayLists.get(7).get(1));
                unopenedCases.remove(arrayListOfArrayLists.get(7).get(0));
                ImageView imgView = (ImageView) arrayListOfArrayLists.get(7).get(3);
                imgView.setImageResource((Integer)arrayListOfArrayLists.get(7).get(2));
                checkCases();
            }
        });
        caseclosed9.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openCaseCount++;
                openedCases.add((Integer) arrayListOfArrayLists.get(8).get(0));
                caseclosed9.setImageResource((Integer) arrayListOfArrayLists.get(8).get(1));
                unopenedCases.remove(arrayListOfArrayLists.get(8).get(0));
                ImageView imgView = (ImageView) arrayListOfArrayLists.get(8).get(3);
                imgView.setImageResource((Integer)arrayListOfArrayLists.get(8).get(2));
                checkCases();
            }
        });
        caseclosed10.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openCaseCount++;
                openedCases.add((Integer) arrayListOfArrayLists.get(9).get(0));
                caseclosed10.setImageResource((Integer) arrayListOfArrayLists.get(9).get(1));
                unopenedCases.remove(arrayListOfArrayLists.get(9).get(0));
                ImageView imgView = (ImageView) arrayListOfArrayLists.get(9).get(3);
                imgView.setImageResource((Integer)arrayListOfArrayLists.get(9).get(2));
                checkCases();
            }
        });
        buttonReset.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = getIntent();
                finish();
                startActivity(intent);
            }
        });
        buttonDeal.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                int total = 0;
                for (int x: unopenedCases) {
                    total += x ;
                }
                currentOffer = total * .6;
                buttonNoDeal.setVisibility(View.INVISIBLE);
                textView.setText("You Win $" + currentOffer);
            }
        });
        buttonNoDeal.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(openCaseCount==4) {
                    textView.setText("Choose 4 Cases");
                }
                if(openCaseCount==8) {
                    textView.setText("Choose 1 Case");
                }
                buttonNoDeal.setVisibility(View.INVISIBLE);
                buttonDeal.setVisibility(View.INVISIBLE);

                for (int viewId : caseClosedIds) {
                    View myView = findViewById(viewId);
                    myView.setClickable(true);    // Set to the original clickable state
                    myView.setFocusable(true);
                    myView.setAlpha(1.0f);
                }
            }
        });
    }
    public void checkCases(){
        if(openCaseCount == 1){
            textView.setText("Choose 3 Cases");
        }else if(openCaseCount == 2){
            textView.setText("Choose 2 Cases");
        }else if(openCaseCount == 3){
            textView.setText("Choose 1 Case");
        }else if(openCaseCount == 5){
            textView.setText("Choose 3 Cases");
        }else if(openCaseCount == 6){
            textView.setText("Choose 2 Cases");
        }else if(openCaseCount == 7){
            textView.setText("Choose 1 Case");
        }

        if (openCaseCount != 4 && openCaseCount != 8) {
            buttonNoDeal.setVisibility(View.INVISIBLE);
            buttonDeal.setVisibility(View.INVISIBLE);
        }

        if (openCaseCount == 4 || openCaseCount == 8) {
            int total = 0;
            for (int x : unopenedCases) {
                total += x;
            }
            currentOffer = total * .6;
            textView.setText("Bank Deal is $" + currentOffer);
            buttonNoDeal.setVisibility(View.VISIBLE);
            buttonDeal.setVisibility(View.VISIBLE);

            for (int viewId : caseClosedIds) {
                View myView = findViewById(viewId);
                myView.setClickable(false);
                myView.setFocusable(false);
                myView.setAlpha(0.5f);
            }
        }

        if(openCaseCount == 9){
            textView.setText("You Win $" + unopenedCases.get(0));
            for (int viewId : caseClosedIds) {
                View myView = findViewById(viewId);
                myView.setClickable(false);
                myView.setFocusable(false);
            }
        }
    }

    private static ArrayList<Object> createArrayList(int number, int open, int reward, ImageView imageView) {
        ArrayList<Object> nestedArrayList = new ArrayList<>();
        nestedArrayList.add(number);
        nestedArrayList.add(open);
        nestedArrayList.add(reward);
        nestedArrayList.add(imageView);
        return nestedArrayList;
    }
}
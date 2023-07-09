package com.example.tilted;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.text.format.Formatter;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.util.ArrayList;

public class FilesActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_files);
        RecyclerView recycler = findViewById(R.id.recycler_view);

        String ip = getIntent().getStringExtra("ip");
        TextView ipTextView = findViewById(R.id.textview_ip);
        ipTextView.setText(ip);

        File root = new File(getIntent().getStringExtra("path"));
        File[] filesAndFolders = root.listFiles();
        if (filesAndFolders != null) {
            ArrayList<File> imagesAndFolders = new ArrayList<>();
            for (File file : filesAndFolders) {
                if (file.isDirectory() || isImage(file)) {
                    imagesAndFolders.add(file);
                }
            }
            recycler.setLayoutManager(new LinearLayoutManager(this));
            recycler.setAdapter(new FilesAdapter(getApplicationContext(), imagesAndFolders, ip));
        }
    }

    private boolean isImage(File file) {
        if (file.getName().contains(".trashed")) return false;
        BitmapFactory.Options options = new BitmapFactory.Options();
        options.inJustDecodeBounds = true;
        Bitmap bitmap = BitmapFactory.decodeFile(file.getAbsolutePath(), options);
        return options.outWidth != -1 && options.outHeight != -1;
    }
}
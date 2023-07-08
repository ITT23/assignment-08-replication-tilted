package com.example.tilted;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.io.File;
import java.util.ArrayList;

public class FilesAdapter extends RecyclerView.Adapter<FilesAdapter.ViewHolder>{

    Context context;
    ArrayList<File> filesAndFolders;

    public FilesAdapter(Context context, ArrayList<File> filesAndFolders) {
        this.context = context;
        this.filesAndFolders = filesAndFolders;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.recycler_item, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        File selectedFile = filesAndFolders.get(position);
        holder.filenameView.setText(selectedFile.getName());
        holder.iconView.setImageResource(selectedFile.isDirectory() ? R.drawable.ic_baseline_folder_24 : R.drawable.ic_baseline_image_24);
        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (selectedFile.isDirectory()) {
                    Intent intent = new Intent(context, FilesActivity.class);
                    String path = selectedFile.getAbsolutePath();
                    intent.putExtra("path", path);
                    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    context.startActivity(intent);
                } else {
                    try {
                        Intent intent = new Intent();
                        intent.setAction(Intent.ACTION_VIEW);
                        intent.setDataAndType(Uri.parse(selectedFile.getAbsolutePath()), "image/*");
                        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                        context.startActivity(intent);
                    } catch (Exception e) {
                        Toast.makeText(context.getApplicationContext(), "Cannot open file. No image file.", Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });
    }

    @Override
    public int getItemCount() {
        return filesAndFolders.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {

        TextView filenameView;
        ImageView iconView;

        public ViewHolder(View itemView) {
            super(itemView);
            filenameView = itemView.findViewById(R.id.filename_view);
            iconView = itemView.findViewById(R.id.icon_view);
        }
    }
}

package com.example.tilted;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;
import androidx.recyclerview.widget.RecyclerView;

import java.io.File;
import java.util.ArrayList;

public class FilesAdapter extends RecyclerView.Adapter<FilesAdapter.ViewHolder>{

    Context context;
    ArrayList<File> filesAndFolders;
    ExplorerFragment fragment;
    MainActivity mainActivity;

    public FilesAdapter(ExplorerFragment fragment) {
        this.fragment = fragment;
        this.context = fragment.getActivity();
        mainActivity = (MainActivity) fragment.getActivity();
        setFiles(fragment.getPath());
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
                fragment.getSender().setCurrentFile(selectedFile);
                try {
                    if (selectedFile.isDirectory()) {
                        fragment.setPath(selectedFile.getAbsolutePath());
                        setFiles(fragment.getPath());
                    } else if (selectedFile.isFile()){
                        mainActivity.setChosenFile(selectedFile);
                        mainActivity.getSender().setCurrentFile(selectedFile);
                        FragmentManager fragmentManager = fragment.getActivity().getSupportFragmentManager();
                        FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
                        fragmentTransaction.replace(R.id.fragment_container, new ImageViewerFragment());
                        fragmentTransaction.addToBackStack(null);
                        fragmentTransaction.commit();
                    }
                } catch (Exception e) {
                    Toast.makeText(context.getApplicationContext(), "Cannot open file. No image file.", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    @Override
    public int getItemCount() {
        return filesAndFolders.size();
    }

    public void setFiles(String path) {
        File root = new File(path);
        File[] filesAndFolders = root.listFiles();
        ArrayList<File> imagesAndFolders = new ArrayList<>();
        if (filesAndFolders != null) {
            for (File file : filesAndFolders) {
                if (file.isDirectory() || isImage(file)) {
                    imagesAndFolders.add(file);
                }
            }
        }
        this.filesAndFolders = imagesAndFolders;
        notifyDataSetChanged();
    }

    private boolean isImage(File file) {
        if (file.getName().contains(".trashed")) return false;
        BitmapFactory.Options options = new BitmapFactory.Options();
        options.inJustDecodeBounds = true;
        Bitmap bitmap = BitmapFactory.decodeFile(file.getAbsolutePath(), options);
        return options.outWidth != -1 && options.outHeight != -1;
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

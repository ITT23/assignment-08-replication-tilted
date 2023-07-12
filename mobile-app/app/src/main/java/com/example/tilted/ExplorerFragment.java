package com.example.tilted;

import android.os.Bundle;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;


public class ExplorerFragment extends Fragment {

    private View view;
    private TextView pathTextview;
    private ImageView navigateBackBtn;
    private RecyclerView recycler;
    private MainActivity mainActivity;
    private String ip;
    private Sender sender;
    private String path;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        view = inflater.inflate(R.layout.fragment_explorer, container, false);
        mainActivity = (MainActivity) getActivity();
        ip = mainActivity.getIp();
        sender = mainActivity.getSender();
        setPath(mainActivity.ROOT_PATH);
        return view;
    }

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        FilesAdapter adapter = new FilesAdapter(ExplorerFragment.this);
        recycler = getView().findViewById(R.id.recycler_view);
        recycler.setLayoutManager(new LinearLayoutManager(mainActivity));
        recycler.setAdapter(adapter);

        navigateBackBtn = getView().findViewById(R.id.back_imageview);
        navigateBackBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (!path.equals(mainActivity.ROOT_PATH)) {
                    setPath(path.substring(0, path.lastIndexOf("/")));
                    adapter.setFiles(path);
                }
            }
        });
        pathTextview = getView().findViewById(R.id.path_textview);
        pathTextview.setText(path);
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
        if (pathTextview != null) pathTextview.setText(path);
    }

    public String getIp() {
        return ip;
    }

    public Sender getSender() {
        return sender;
    }
}
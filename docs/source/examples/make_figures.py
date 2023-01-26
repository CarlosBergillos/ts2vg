from basic import ax1, ax2, fig

ax1.margins(x=0, y=0)
ax2.margins(x=0, y=0)
fig.tight_layout(w_pad=3)
fig.savefig("basic.png", facecolor=(0, 0, 0, 0), bbox_inches="tight")


from degree_distribution import fig

fig.tight_layout(w_pad=2)
fig.savefig("degree_distribution.svg", facecolor=(0, 0, 0, 0), bbox_inches="tight")


from directed import fig

fig.tight_layout(w_pad=2)
fig.savefig("directed.svg", facecolor=(0, 0, 0, 0), bbox_inches="tight")


from weighted import fig

fig.tight_layout(w_pad=2)
fig.subplots_adjust(right=0.94)
fig.savefig("weighted.svg", facecolor=(0, 0, 0, 0), bbox_inches="tight")


from horizontal import fig

fig.tight_layout(w_pad=2)
fig.savefig("horizontal.svg", facecolor=(0, 0, 0, 0), bbox_inches="tight")


from partitioning import ax1, ax2, fig

ax1.margins(x=0, y=0)
ax2.margins(x=0, y=0)
fig.tight_layout(w_pad=3)
fig.savefig("partitioning.png", facecolor=(0, 0, 0, 0), bbox_inches="tight")

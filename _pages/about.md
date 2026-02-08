---
layout: page
title: About
permalink: /about/
body_class: page-network
nav: true
nav_order: 2
---

<style>
.network-text {
  text-align: justify;
  text-justify: inter-word;
  hyphens: auto;
}
</style>

<style>
/* Justify text inside WP boxes */
#wpAccordion .card-body {
  text-align: justify;
  text-justify: inter-word;
  hyphens: auto;
}
</style>

<div class="network-text" markdown="1">

The scientific programme of **STRONG** is structured into four tightly connected work packages (WPs), 
each addressing a key challenge in strong-field gravity and gravitational-wave physics. Together, 
they span environmental effects, extensions of General Relativity, exotic compact objects, and 
data-analysis strategies for current and future detectors.

Click on each work package below to explore its scientific scope.Click on each work package below to explore its scientific scope and objectives.

</div>

<style>
/* Grid cards: rounded corners + subtle spacing */
.wp-grid .wp-card {
  border-radius: 14px;
  overflow: hidden;            /* ensures rounded corners apply to header/body */
  border: 2px solid;           /* color set per WP below */
  height: 100%;
}

.wp-grid .wp-card .card-header {
  background: transparent;
  border-bottom: 1px solid rgba(0,0,0,0.08);
  font-weight: 700;
}

.wp-grid .wp-card .card-body {
  text-align: justify;
  text-justify: inter-word;
  hyphens: auto;
  line-height: 1.45;
}

/* Colored contours (adjust colors if you want) */
.wp1 { border-color: #2E7D32; } /* green */
.wp2 { border-color: #1565C0; } /* blue */
.wp3 { border-color: #6A1B9A; } /* purple */
.wp4 { border-color: #C62828; } /* red */

/* Optional: matching left accent bar inside header */
.wp-grid .wp-card .card-header {
  position: relative;
  padding-left: 1.1rem;
}
.wp-grid .wp-card .card-header::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 8px;
  background: currentColor;
  opacity: 0.9;
}
.wp1 { color: #2E7D32; }
.wp2 { color: #1565C0; }
.wp3 { color: #6A1B9A; }
.wp4 { color: #C62828; }

/* Keep body text normal color */
.wp-grid .wp-card .card-body { color: inherit; }
</style>

<div class="row wp-grid">

  <div class="col-md-6 mb-4">
    <div class="card wp-card wp1">
      <div class="card-header">
        WP1 — Environmental effects in extreme gravity regimes
      </div>
      <div class="card-body">
        WP1 investigates the interplay between matter fields and black holes in strong-gravity regimes. The work package focuses on developing a comprehensive relativistic framework for black-hole solutions embedded in realistic astrophysical environments, with the goal of characterising their physical properties and dynamical behaviour.

        A central objective of WP1 is to assess how environmental effects modify gravitational-wave emission, particularly during merger events. By modelling these effects in both asymmetric and comparable-mass systems, WP1 provides essential input for waveform construction and for the interpretation of gravitational-wave observations in realistic astrophysical settings.
      </div>
    </div>
  </div>

  <div class="col-md-6 mb-4">
    <div class="card wp-card wp2">
      <div class="card-header">
        WP2 — Gravity beyond General Relativity and fundamental fields
      </div>
      <div class="card-body">
        WP2 addresses gravitational-wave signatures of theories beyond General Relativity, with particular emphasis on the role of additional fundamental fields. The objective is to develop accurate waveform models that describe the full coalescence of binary black holes in selected beyond-GR scenarios.

        This work package combines numerical relativity and perturbative techniques to cover the mass range relevant for future gravitational-wave detectors. In parallel, WP2 develops novel effective-field-theory approaches specifically tailored to asymmetric binaries, which are prime targets for space-based observatories.
      </div>
    </div>
  </div>

  <div class="col-md-6 mb-4">
    <div class="card wp-card wp3">
      <div class="card-header">
        WP3 — Coherent models of Exotic Compact Objects
      </div>
      <div class="card-body">
        WP3 is dedicated to the modelling of Exotic Compact Objects (ECOs) and to the construction of the first full-coalescence gravitational-wave signals for these systems. The aim is to capture deviations from the Kerr black-hole paradigm across all phases of the coalescence process.

        The work focuses on concrete and well-motivated models—such as scalar and vector boson stars and topological stars—for which members of the STRONG consortium have already produced seminal results. By exploring the parameter space of these models, WP3 seeks to span a broad and representative family of black-hole mimickers and to identify robust observational signatures of their exotic nature.
      </div>
    </div>
  </div>

  <div class="col-md-6 mb-4">
    <div class="card wp-card wp4">
      <div class="card-header">
        WP4 — Data analysis for fundamental fields and GW sources
      </div>
      <div class="card-body">
        WP4 integrates the waveform models developed in WPs 1–3 into advanced data-analysis pipelines for gravitational-wave observations. The work package extends existing inference frameworks with new algorithms for parameter estimation and model selection, tailored to both comparable-mass and asymmetric systems.

        For comparable-mass binaries, WP4 builds on the Bilby framework, while dedicated inference tools based on FEW are developed for asymmetric binaries. Analyses are performed using simulated data from next-generation space- and ground-based detectors, supported by astrophysically motivated source catalogues. All tools are released to the community to maximise scientific impact and enable direct application to LVK data.
      </div>
    </div>
  </div>

</div>

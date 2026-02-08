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
/* === WP GRID STYLING === */

.wp-grid .wp-card {
  border-radius: 14px;
  border: 2px solid;
  height: 100%;
  overflow: hidden;
  box-shadow: none !important;
  background: #fff;
}

/* Header */
.wp-grid .wp-card .card-header {
  background: transparent;
  border-bottom: 1px solid rgba(0,0,0,0.08);
  font-weight: 700;
  padding: 0.75rem 1rem;
}

/* Body text */
.wp-grid .wp-card .card-body {
  text-align: justify;
  text-justify: inter-word;
  hyphens: auto;
  line-height: 1.45;
  color: #000;
  padding: 1rem;
}

/* Colored borders (only) */
.wp1 { border-color: #2E7D32; }
.wp2 { border-color: #1565C0; }
.wp3 { border-color: #6A1B9A; }
.wp4 { border-color: #C62828; }
</style>

<div class="row wp-grid">

  <!-- WP1 -->
  <div class="col-md-6 mb-4">
    <div class="card wp-card wp1">
      <div class="card-header">
        WP1 — Environmental effects in extreme gravity regimes
      </div>
      <div class="card-body">
      WP1 investigates the interplay between matter fields and black holes in strong-gravity regimes. 
      The work package focuses on developing a comprehensive relativistic framework for black-hole 
      solutions embedded in realistic astrophysical environments, with the goal of characterising 
      their physical properties and dynamical behaviour. A central objective of WP1 is to assess 
      how environmental effects modify gravitational-wave emission, particularly during merger events. 
      By modelling these effects in both asymmetric and comparable-mass systems, WP1 provides 
      essential input for waveform construction and for the interpretation of gravitational-wave
       observations in realistic astrophysical settings.      
      </div>
    </div>
  </div>

  <!-- WP2 -->
  <div class="col-md-6 mb-4">
    <div class="card wp-card wp2">
      <div class="card-header">
        WP2 — Gravity beyond General Relativity and fundamental fields
      </div>
      <div class="card-body">
        WP2 addresses gravitational-wave signatures of theories beyond General Relativity, 
        and the role of additional fundamental fields. The objective is to develop accurate 
        waveform models that describe the full coalescence of binary black holes in 
        beyond-GR scenarios. This work package combines numerical relativity and perturbative 
        techniques to cover the mass range relevant for current and future gravitational-wave 
        detectors. In parallel, WP2 develops novel effective-field-theory approaches specifically 
        tailored to asymmetric binaries, which are prime targets for space-based observatories.
      </div>
    </div>
  </div>

  <!-- WP3 -->
  <div class="col-md-6 mb-4">
    <div class="card wp-card wp3">
      <div class="card-header">
        WP3 — Coherent models of Exotic Compact Objects
      </div>
      <div class="card-body">
        WP3 is dedicated to the modelling of Exotic Compact Objects (ECOs) and to the construction 
        of the first full-coalescence gravitational-wave signals emitted by ECO binaries. The aim 
        is to capture deviations from the Kerr black-hole paradigm across all phases of the coalescence process.
        The WP focuses on concrete and well-motivated models for which members of the STRONG consortium have 
        already produced seminal results. By exploring the parameter space of these models, WP3 seeks to span 
        a broad and representative family of black-hole mimickers and to identify robust observational 
        signatures of their exotic nature.
      </div>
    </div>
  </div>

  <!-- WP4 -->
  <div class="col-md-6 mb-4">
    <div class="card wp-card wp4">
      <div class="card-header">
        WP4 — Data analysis for fundamental fields and GW sources
      </div>
      <div class="card-body">
 WP4 integrates the waveform models developed in WPs 1–3 into advanced data-analysis 
        pipelines for gravitational-wave observations. The work package extends existing 
        inference frameworks with new algorithms for parameter estimation and model selection, 
        tailored to both comparable-mass and asymmetric systems. Analyses are conducted 
        using simulated data from next-generation space- and ground-based detectors, 
        supported by astrophysically motivated source catalogues. All tools are released 
        to the community to maximise scientific impact and enable direct application to current 
        data by LIGO/Virgo/KAGRA detectors.         </div>
    </div>
  </div>

</div>

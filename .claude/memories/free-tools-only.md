---
name: free-tools-only
description: Nothing used to make a production in this repo may cost money; no paid services, subscriptions, or metered APIs, for voice or anything else
metadata:
  type: feedback
---

# Free tools only

Everything used to make a production in this repo must be free. Nothing paid is offered, even as one alternative among several.

**Why:** It is the user's rule, and no reason comes with it.

**How to apply:** Do not propose or wire in paid services, subscriptions, or metered APIs, for narration, music, images, or tooling. Offer only open-source models that run on the free GitHub runners, free assets with a licence that allows use in a published video, or work done by a person at no cost (the user recording the narration, for example). Check the licence before proposing a model or asset: free to download is not the same as free to use in a published video. Check the model's weights as well as its code, and say up front whether a credit is required: Pocket TTS, for example, has MIT-licensed code and CC BY 4.0 weights, so a film that uses one of its voices owes a credit. Claude's interpretation, not confirmed as a rule: the user prefers options with no attribution requirement, so list those first and mark any credit requirement plainly. Claude's interpretation: a service that is free of charge but only through an unofficial or terms-breaking route does not count as free, so name the catch if one is ever raised. Hyperframes, which renders the scenes, is used for its renderer alone, under the Apache 2.0 licence: its maker's paid voices, avatars, and cloud renders are not used, and neither is GSAP, the animation library its examples use, which costs nothing but is not open source. Related: [Video production decisions](video-production-decisions.md).

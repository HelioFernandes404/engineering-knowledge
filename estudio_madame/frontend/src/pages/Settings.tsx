import { useState } from 'react';
import { Upload } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';

const Settings = () => {
  const [notifications, setNotifications] = useState({
    clientSelections: true,
    clientApprovals: true,
    newComments: false,
  });

  return (
    <div className="container max-w-7xl mx-auto px-6 pt-10">
      {/* Header */}
      <header className="mb-10">
        <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">Settings</h1>
      </header>

      <div className="space-y-8">
        {/* Profile Information */}
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl font-bold">Profile Information</CardTitle>
            <CardDescription>Update your personal details here.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="fullName">Full Name</Label>
                <Input
                  id="fullName"
                  placeholder="Enter your full name"
                  defaultValue="John Doe"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email Address</Label>
                <Input
                  id="email"
                  type="email"
                  defaultValue="john.doe@example.com"
                  disabled
                  className="cursor-not-allowed opacity-60"
                />
              </div>
            </div>
            <Separator />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="newPassword">New Password</Label>
                <Input
                  id="newPassword"
                  type="password"
                  placeholder="Enter new password"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Confirm New Password</Label>
                <Input
                  id="confirmPassword"
                  type="password"
                  placeholder="Confirm new password"
                />
              </div>
            </div>
          </CardContent>
          <CardFooter className="border-t pt-6 flex justify-end">
            <Button>Save Changes</Button>
          </CardFooter>
        </Card>

        {/* Notification Settings */}
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl font-bold">Notification Settings</CardTitle>
            <CardDescription>Manage your email notifications.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center justify-between space-x-4">
              <div className="flex-1 space-y-1">
                <Label htmlFor="client-selections" className="text-base font-medium">
                  Client makes new selections
                </Label>
                <p className="text-sm text-muted-foreground">
                  Receive an email when a client finalizes their photo selections.
                </p>
              </div>
              <Switch
                id="client-selections"
                checked={notifications.clientSelections}
                onCheckedChange={(checked) =>
                  setNotifications({ ...notifications, clientSelections: checked })
                }
              />
            </div>
            <Separator />
            <div className="flex items-center justify-between space-x-4">
              <div className="flex-1 space-y-1">
                <Label htmlFor="client-approvals" className="text-base font-medium">
                  Client approves a gallery
                </Label>
                <p className="text-sm text-muted-foreground">
                  Get notified when a client gives final approval on a gallery.
                </p>
              </div>
              <Switch
                id="client-approvals"
                checked={notifications.clientApprovals}
                onCheckedChange={(checked) =>
                  setNotifications({ ...notifications, clientApprovals: checked })
                }
              />
            </div>
            <Separator />
            <div className="flex items-center justify-between space-x-4">
              <div className="flex-1 space-y-1">
                <Label htmlFor="new-comments" className="text-base font-medium">
                  New comment on a photo
                </Label>
                <p className="text-sm text-muted-foreground">
                  Receive an email for each new comment on photos in a gallery.
                </p>
              </div>
              <Switch
                id="new-comments"
                checked={notifications.newComments}
                onCheckedChange={(checked) =>
                  setNotifications({ ...notifications, newComments: checked })
                }
              />
            </div>
          </CardContent>
        </Card>

        {/* Billing & Subscription */}
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl font-bold">Billing & Subscription</CardTitle>
            <CardDescription>Manage your plan and billing details.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div>
                <p className="text-sm font-medium">
                  Current Plan: <span className="text-lg font-bold text-primary">Pro Plan</span>
                </p>
                <p className="text-sm text-muted-foreground mt-1">
                  Your plan renews on December 1, 2024.
                </p>
              </div>
              <Button variant="outline">Manage Subscription</Button>
            </div>
          </CardContent>
        </Card>

        {/* Custom Branding */}
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl font-bold">Custom Branding</CardTitle>
            <CardDescription>Customize the look of your client galleries.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <Label>Custom Logo</Label>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-start">
                <div className="md:col-span-2">
                  <label
                    htmlFor="logo-upload"
                    className="flex flex-col items-center justify-center w-full h-40 border-2 border-dashed rounded-lg cursor-pointer bg-muted/50 hover:bg-muted transition-colors"
                  >
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                      <Upload className="w-8 h-8 mb-4 text-muted-foreground" />
                      <p className="mb-2 text-sm text-muted-foreground">
                        <span className="font-semibold">Click to upload</span> or drag and drop
                      </p>
                      <p className="text-xs text-muted-foreground">
                        SVG, PNG, JPG or GIF (MAX. 800x400px)
                      </p>
                    </div>
                    <input id="logo-upload" type="file" className="hidden" accept="image/*" />
                  </label>
                </div>
                <div className="md:col-span-1">
                  <Label className="text-xs text-muted-foreground mb-2 block">Logo Preview</Label>
                  <div className="w-full aspect-video rounded-lg bg-muted/50 border flex items-center justify-center">
                    <p className="text-sm text-muted-foreground">No logo uploaded</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
          <CardFooter className="border-t pt-6 flex justify-end">
            <Button>Save Branding</Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
};

export default Settings;
